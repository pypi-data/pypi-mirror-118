import attr
from oauth2_client.credentials_manager import CredentialManager, ServiceInformation
from structlog import get_logger

from data_point_client import AuthenticatedClient
from data_point_client.api.data_point import data_point_get_data_2

from .gnista_credential_manager import GnistaCredentialManager

log = get_logger()


class GnistaConnection:
    scope = ["data-api"]

    def __init__(self, base_url: str = "https://aws.gnista.io", refresh_token: str = None):
        self.base_url = base_url
        self.access_token = None
        self.id_token = None
        self.tenant_name = None
        self.refresh_token = refresh_token

    def get_access_token(self) -> str:
        if (self.access_token == None or self.id_token == None) and self.refresh_token == None:
            # Initial create of tokens
            self._create_tokens()
        else:
            # refresh with existing refresh token
            self._refresh_tokens(refresh_token=self.refresh_token)
        return self.access_token

    def _get_service_info(self, scope: list = scope) -> ServiceInformation:
        return ServiceInformation(
            self.base_url + "/authentication/connect/authorize",
            self.base_url + "/authentication/connect/token",
            "python",
            "",
            scope,
            False,
        )

    def _refresh_tokens(self, refresh_token: str):
        service_information = self._get_service_info()
        manager = GnistaCredentialManager(service_information)
        manager.init_with_token(refresh_token)

        self.tenant_name = manager.tenant_name
        self.access_token = manager._access_token
        self.refresh_token = manager.refresh_token
        self.id_token = manager.id_token

    def _create_tokens(self, scope: list = scope):
        scope.append("openid")
        scope.append("profile")
        scope.append("offline_access")

        service_information = self._get_service_info(scope)

        manager = GnistaCredentialManager(service_information)
        # manager.init_with_client_credentials()
        redirect_uri = "http://localhost:4200/home"
        url = manager.init_authorize_code_process(redirect_uri=redirect_uri, state="myState")
        log.info("Authentication has been started. Please follow the link to authenticate with your user:", url=url)

        code = manager.wait_and_terminate_authorize_code_process()
        # From this point the http server is opened on 8080 port and wait to receive a single GET request
        # All you need to do is open the url and the process will go on
        # (as long you put the host part of your redirect uri in your host file)
        # when the server gets the request with the code (or error) in its query parameters
        manager.init_with_authorize_code(redirect_uri, code)
        # Here access and refresh token may be used with self.refresh_token
        self.tenant_name = manager.tenant_name
        self.access_token = manager._access_token
        self.refresh_token = manager.refresh_token
        self.id_token = manager.id_token
