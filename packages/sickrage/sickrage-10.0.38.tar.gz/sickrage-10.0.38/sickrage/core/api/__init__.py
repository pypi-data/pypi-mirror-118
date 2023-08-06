import collections
import errno
import time
import traceback
from urllib.parse import urljoin

import oauthlib.oauth2
import requests
import requests.exceptions
from jose import ExpiredSignatureError
from oauthlib.oauth2 import MissingTokenError, InvalidGrantError, InvalidClientIdError
from requests_oauthlib import OAuth2Session
from sqlalchemy import orm

import sickrage
from sickrage.core.api.exceptions import APIError
from sickrage.core.databases.cache import CacheDB


class API(object):
    def __init__(self):
        self.name = 'SR-API'
        self.api_base = 'https://www.sickrage.ca/api/'
        self.api_version = 'v6'
        self._session = None

    @property
    def is_enabled(self):
        return self.token

    @property
    def imdb(self):
        return self.IMDbAPI(self)

    @property
    def server(self):
        return self.ServerAPI(self)

    @property
    def provider(self):
        return self.ProviderAPI(self)

    @property
    def announcement(self):
        return self.AnnouncementsAPI(self)

    @property
    def google(self):
        return self.GoogleDriveAPI(self)

    @property
    def torrent(self):
        return self.TorrentAPI(self)

    @property
    def scene_exceptions(self):
        return self.SceneExceptions(self)

    @property
    def alexa(self):
        return self.AlexaAPI(self)

    @property
    def session(self):
        extra = {
            'client_id': sickrage.app.auth_server.client_id,
        }

        if not self._session and self.token_url:
            self._session = OAuth2Session(token=self.token, auto_refresh_kwargs=extra, auto_refresh_url=self.token_url, token_updater=self.token_updater)

        return self._session

    @property
    def token(self):
        session = sickrage.app.cache_db.session()

        try:
            token = session.query(CacheDB.OAuth2Token).one()
            return token.as_dict()
        except orm.exc.NoResultFound:
            return {}

    @token.setter
    def token(self, value):
        new_token = {
            'access_token': value.get('access_token'),
            'refresh_token': value.get('refresh_token'),
            'expires_in': value.get('expires_in'),
            'session_state': value.get('session_state'),
            'token_type': value.get('token_type'),
            'expires_at': value.get('expires_at', int(time.time() + value.get('expires_in'))),
            'scope': value.scope if isinstance(value, oauthlib.oauth2.OAuth2Token) else value.get('scope'),
        }

        session = sickrage.app.cache_db.session()

        try:
            token = session.query(CacheDB.OAuth2Token).one()
            token.update(**new_token)
        except orm.exc.NoResultFound:
            session.add(CacheDB.OAuth2Token(**new_token))
        finally:
            session.commit()

        self._session = None

    @token.deleter
    def token(self):
        session = sickrage.app.cache_db.session()
        session.query(CacheDB.OAuth2Token).delete()
        session.commit()

    @property
    def token_expiration(self):
        try:
            certs = sickrage.app.auth_server.certs()
            if not certs:
                return time.time()

            decoded_token = sickrage.app.auth_server.decode_token(self.token['access_token'], certs)
            return decoded_token.get('exp', time.time())
        except ExpiredSignatureError:
            return time.time()

    @property
    def token_time_remaining(self):
        return max(self.token_expiration - time.time(), 0)

    @property
    def token_is_expired(self):
        return self.token_expiration <= time.time()

    @property
    def token_url(self):
        return sickrage.app.auth_server.get_url('token_endpoint')

    @property
    def health(self):
        for i in range(3):
            try:
                health = requests.get(urljoin(self.api_base, "health"), verify=False, timeout=30).ok
            except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
                pass
            else:
                break
        else:
            health = False

        if not health:
            sickrage.app.log.debug("SiCKRAGE API is currently unreachable")
            return False

        return True

    @property
    def userinfo(self):
        return self.request('GET', 'userinfo')

    def token_updater(self, value):
        self.token = value

    def logout(self):
        sickrage.app.auth_server.logout(self.token.get('refresh_token'))

    def refresh_token(self):
        extra = {
            'client_id': sickrage.app.auth_server.client_id,
        }

        if self.token_url:
            try:
                client = OAuth2Session(sickrage.app.auth_server.client_id, token=self.token)
                self.token = client.refresh_token(self.token_url, **extra)
                return True
            except (InvalidGrantError, MissingTokenError, InvalidClientIdError, requests.exceptions.RequestException):
                return False

        return False

    def exchange_token(self, access_token, scope='offline_access'):
        exchange = {'scope': scope, 'subject_token': access_token}
        exchanged_token = sickrage.app.auth_server.token_exchange(**exchange)
        if exchanged_token:
            self.token = exchanged_token

    def allowed_usernames(self):
        return self.request('GET', 'allowed-usernames')

    def download_privatekey(self):
        return self.request('GET', 'server/config/private-key')

    def upload_privatekey(self, privatekey):
        return self.request('POST', 'server/config/private-key', data=dict({'privatekey': privatekey}))

    def network_timezones(self):
        return self.request('GET', 'network-timezones')

    def request(self, method, url, timeout=120, **kwargs):
        if not self.is_enabled or not self.session:
            return

        url = urljoin(self.api_base, "/".join([self.api_version, url]))

        for i in range(5):
            resp = None

            try:
                if not self.health:
                    if i > 3:
                        return None
                    continue

                if self.token_time_remaining < (int(self.token['expires_in']) / 2):
                    if not self.refresh_token():
                        continue

                resp = self.session.request(method, url, timeout=timeout, verify=False, hooks={'response': self.throttle_hook}, **kwargs)

                resp.raise_for_status()
                if resp.status_code == 204:
                    return resp.ok

                try:
                    return resp.json()
                except ValueError:
                    return resp.content
            except oauthlib.oauth2.TokenExpiredError:
                self.refresh_token()
                time.sleep(1)
            except (oauthlib.oauth2.InvalidClientIdError, oauthlib.oauth2.MissingTokenError, oauthlib.oauth2.InvalidGrantError) as e:
                sickrage.app.log.warning("Invalid token error, please re-link your SiCKRAGE account from `settings->general->advanced->sickrage api`")
                return
            except requests.exceptions.ReadTimeout as e:
                if i > 3:
                    sickrage.app.log.debug(f'Error connecting to url {url} Error: {e}')
                    return resp or e.response

                timeout += timeout
                time.sleep(1)
            except requests.exceptions.HTTPError as e:
                status_code = e.response.status_code
                error_message = e.response.text

                if status_code == 403 and "login-pf-page" in error_message:
                    self.refresh_token()
                    time.sleep(1)
                    continue

                if 'application/json' in e.response.headers.get('content-type', ''):
                    status_code = e.response.json().get('error', status_code)
                    error_message = e.response.json().get('message', error_message)
                    sickrage.app.log.debug(f'SiCKRAGE API response returned for url {url} Response: {error_message}, Code: {status_code}')
                else:
                    sickrage.app.log.debug(f'The response returned a non-200 response while requesting url {url} Error: {e!r}')

                return resp or e.response
            except requests.exceptions.ConnectionError as e:
                if i > 3:
                    sickrage.app.log.debug(f'Error connecting to url {url} Error: {e}')
                    return resp or e.response

                time.sleep(1)
            except requests.exceptions.RequestException as e:
                sickrage.app.log.debug(f'Error requesting url {url} Error: {e}')
                return resp or e.response
            except Exception as e:
                if (isinstance(e, collections.Iterable) and 'ECONNRESET' in e) or (getattr(e, 'errno', None) == errno.ECONNRESET):
                    sickrage.app.log.warning(f'Connection reset by peer accessing url {url} Error: {e}')
                else:
                    sickrage.app.log.info(f'Unknown exception in url {url} Error: {e}')
                    sickrage.app.log.debug(traceback.format_exc())

                return None

    @staticmethod
    def throttle_hook(response, **kwargs):
        if "X-RateLimit-Remaining" in response.headers:
            remaining = int(response.headers["X-RateLimit-Remaining"])
            if remaining == 1:
                sickrage.app.log.debug("Throttling SiCKRAGE API Calls... Sleeping for 60 secs...\n")
                time.sleep(60)

    class ServerAPI:
        def __init__(self, api):
            self.api = api

        def register_server(self, ip_addresses, web_protocol, web_port, web_root, server_version):
            data = {
                'ip-addresses': ip_addresses,
                'web-protocol': web_protocol,
                'web-port': web_port,
                'web-root': web_root,
                'server-version': server_version
            }

            return self.api.request('POST', 'server', data=data)

        def unregister_server(self, server_id):
            data = {
                'server-id': server_id
            }

            return self.api.request('DELETE', 'server', data=data)

        def update_server(self, server_id, ip_addresses, web_protocol, web_port, web_root, server_version):
            data = {
                'server-id': server_id,
                'ip-addresses': ip_addresses,
                'web-protocol': web_protocol,
                'web-port': web_port,
                'web-root': web_root,
                'server-version': server_version
            }

            return self.api.request('PUT', 'server', data=data)

        def get_status(self, server_id):
            return self.api.request('GET', f'server/{server_id}/status')

        def get_server_certificate(self, server_id):
            return self.api.request('GET', f'server/{server_id}/certificate')

        def declare_amqp_queue(self, server_id):
            return self.api.request('GET', f'server/{server_id}/declare-amqp-queue')

        def upload_config(self, server_id, pkey_sig, config):
            data = {
                'server-id': server_id,
                'pkey-sig': pkey_sig,
                'config': config
            }
            return self.api.request('POST', f'server/{server_id}/config', data=data)

        def download_config(self, server_id, pkey_sig):
            data = {
                'pkey-sig': pkey_sig
            }

            return self.api.request('GET', f'server/{server_id}/config', json=data)['config']

    class AnnouncementsAPI:
        def __init__(self, api):
            self.api = api

        def get_announcements(self):
            return self.api.request('GET', 'announcements')

    class ProviderAPI:
        def __init__(self, api):
            self.api = api

        def get_urls(self, provider):
            query = f'provider/{provider}/urls'
            return self.api.request('GET', query)

        def get_status(self, provider):
            query = f'provider/{provider}/status'
            return self.api.request('GET', query)

        def get_search_result(self, provider, series_id, season, episode):
            query = f'provider/{provider}/series-id/{series_id}/season/{season}/episode/{episode}'
            return self.api.request('GET', query)

        def add_search_result(self, provider, data):
            return self.api.request('POST', f'provider/{provider}', json=data)

    class TorrentAPI:
        def __init__(self, api):
            self.api = api

        def get_trackers(self):
            query = f'torrent/trackers'
            return self.api.request('GET', query)

        def get_torrent(self, hash):
            query = f'torrent/{hash}'
            return self.api.request('GET', query)

        def add_torrent(self, url):
            return self.api.request('POST', 'torrent', json={'url': url})

    class IMDbAPI:
        def __init__(self, api):
            self.api = api

        def search_by_imdb_title(self, title):
            query = f'imdb/search-by-title/{title}'
            return self.api.request('GET', query)

        def search_by_imdb_id(self, imdb_id):
            query = f'imdb/search-by-id/{imdb_id}'
            return self.api.request('GET', query)

    class GoogleDriveAPI:
        def __init__(self, api):
            self.api = api

        def is_connected(self):
            query = 'google-drive/is-connected'
            return self.api.request('GET', query)

        def upload(self, file, folder):
            query = 'google-drive/upload'
            return self.api.request('POST', query, files={'file': open(file, 'rb')}, params={'folder': folder})

        def download(self, id):
            query = f'google-drive/download/{id}'
            return self.api.request('GET', query)

        def delete(self, id):
            query = f'google-drive/delete/{id}'
            return self.api.request('GET', query)

        def search_files(self, id, term):
            query = f'google-drive/search-files/{id}/{term}'
            return self.api.request('GET', query)

        def list_files(self, id):
            query = f'google-drive/list-files/{id}'
            return self.api.request('GET', query)

        def clear_folder(self, id):
            query = f'google-drive/clear-folder/{id}'
            return self.api.request('GET', query)

    class SceneExceptions:
        def __init__(self, api):
            self.api = api

        def get(self, *args, **kwargs):
            query = 'scene-exceptions'
            return self.api.request('GET', query)

        def search_by_id(self, series_id):
            query = f'scene-exceptions/search-by-id/{series_id}'
            return self.api.request('GET', query)

    class AlexaAPI:
        def __init__(self, api):
            self.api = api

        def send_notification(self, message):
            return self.api.request('POST', 'alexa/notification', json={'message': message})
