from google.cloud import compute_v1
import configparser


config = configparser.ConfigParser()
config.read('config.ini')
project = config["gcp"]["project_id"]



def ssl_create_managed(certificate_name, domains):
    client = compute_v1.SslCertificatesClient()

    ssl_certificate = compute_v1.SslCertificate(
        name=certificate_name,
        managed=compute_v1.SslCertificateManagedSslCertificate(
            domains=domains
        ),
        type="MANAGED"
    )
    request = compute_v1.InsertSslCertificateRequest(
        project=project,
        ssl_certificate_resource=ssl_certificate
    )

    response = client.insert(request=request)
    response = response.result()
    return response


def ssl_delete(certificate_name):
    client = compute_v1.SslCertificatesClient()

    request = {
        "project": project,
        "ssl_certificate": certificate_name,
    }

    try:
        # Make the delete request
        response = client.delete(request=request)
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")


def ssl_get_managed_domains(certificate_name):
    client = compute_v1.SslCertificatesClient()

    # Initialize request argument(s)
    if certificate_name.startswith("https://www.googleapis.com/compute/v1/projects/"):
        certificate_name = certificate_name.split("/")[-1]

    request = compute_v1.GetSslCertificateRequest(
        project=project,
        ssl_certificate=certificate_name,
    )

    # Make the request
    response = client.get(request=request)

    # Handle the response
    return response.creation_timestamp, response.managed.domains

