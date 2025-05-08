import requests


class HTTPRequest:
    def __init__(self, url, auth_token=None, user_agent=None):
        """
        Initializes the HTTPRequest class with a URL, authentication token, and user-agent.

        :param url: API endpoint
        :param auth_token: (Optional) Bearer token for authentication
        :param user_agent: (Optional) Custom user-agent
        """
        self.url = url
        self.auth_token = auth_token
        self.user_agent = user_agent

    def _get_headers(self, custom_headers=None):
        """Generates default headers with authentication and User-Agent."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "application/json",
        }

        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"

        if custom_headers:
            headers.update(custom_headers)  # Merge custom headers

        return headers

    def http_method(self, method, data=None, headers=None):
        """
        Sends an HTTP request using the specified method.

        :param method: HTTP method (GET, POST, PUT, DELETE)
        :param data: (Optional) Data to send in request body (for POST/PUT)
        :param headers: (Optional) Custom headers
        :return: Response text or error message
        """
        try:
            response = None
            headers = self._get_headers(headers)

            if method == "GET":
                response = requests.get(self.url, headers=headers, verify=False)  # verify is false for testing
            elif method == "POST":
                response = requests.post(self.url, json=data, headers=headers, verify=True)
            elif method == "PUT":
                response = requests.put(self.url, json=data, headers=headers, verify=True)
            elif method == "DELETE":
                response = requests.delete(self.url, json=data, headers=headers, verify=True)

            # Handle response status codes
            if response is None:
                return "Error: No response received."

            status_code = response.status_code

            if status_code == 200:
                return response.text
            elif status_code == 201:
                return "Success: Resource created successfully."
            elif status_code == 204:
                return "Success: No content (Action successful but no response body)."
            elif status_code == 400:
                return f"Bad Request: The server could not understand the request. {response.text}"
            elif status_code == 401:
                return "Unauthorized: Invalid or missing authentication credentials."
            elif status_code == 403:
                return "Forbidden: You do not have permission to access this resource."
            elif status_code == 404:
                return "Not Found: The requested resource could not be found."
            elif status_code == 500:
                return "Internal Server Error: The server encountered an unexpected condition."
            elif status_code == 502:
                return "Bad Gateway: The server received an invalid response from the upstream server."
            elif status_code == 503:
                return "Service Unavailable: The server is currently unable to handle the request."
            elif status_code == 504:
                return "Gateway Timeout: The server did not receive a timely response from an upstream server."
            else:
                return f"Unexpected Error ({status_code}): {response.text}"

        except requests.exceptions.SSLError as e:
            return f"SSL Error: {e}"
        except requests.exceptions.ConnectionError:
            return "Connection Error: Unable to connect to the server."
        except requests.exceptions.Timeout:
            return "Timeout Error: The request took too long to complete."
        except requests.exceptions.RequestException as e:
            return f"Request Exception: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
