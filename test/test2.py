import datetime

certificates = {
'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/test-3-certificate': ['2023-10-04T04:38:14.477-07:00', ['sstcloud.tagmate.app', 'sst.tatvic.net']], 
'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-b8qyyzrguu': ['2023-11-07T03:04:57.170-08:00', ['sstcloud.tagmate.app', 'sst.tatvic.net', 'deeptest.com']], 
'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-5fwiduafr2': ['2023-11-07T03:11:25.068-08:00', ['sstcloud.tagmate.app', 'sst.tatvic.net', 'interntest.com']],
 'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-ufm3ao6nmi': ['2023-11-07T03:28:52.277-08:00', ['sstcloud.tagmate.app', 'sst.tatvic.net', 'testtest.com']]}

latest_certificate = None
latest_timestamp = None

for certificate, data in certificates.items():
    timestamp = data[0]
    if latest_timestamp is None or timestamp > latest_timestamp:
        latest_certificate = certificate
        latest_timestamp = timestamp

# Merge domains of all previous certificates into the latest one
if latest_certificate:
    domains_to_merge = []
    for certificate, data in certificates.items():
        if certificate != latest_certificate:
            domains_to_merge.extend(data[1])

    certificates[latest_certificate][1].extend(domains_to_merge)
    certificates[latest_certificate][1] = list(set(certificates[latest_certificate][1]))

    new_certificate_domains= list(certificates[latest_certificate][1])
    new_certificate_domains.append("new_domain")
    f_certificates=[]
    f_certificates = list(certificates.keys())
    new_certificate = f'https://www.googleapis.com/compute/v1/projects/{"project"}/global/sslCertificates/{"certificate_name"}'
    f_certificates.append(new_certificate)

print(f_certificates,certificates[latest_certificate][1])




['https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/test-3-certificate', 
 'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-b8qyyzrguu', 
 'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-5fwiduafr2', 
 'https://www.googleapis.com/compute/v1/projects/server-side-tagging-392006/global/sslCertificates/sst-certificate-ufm3ao6nmi', 
 'https://www.googleapis.com/compute/v1/projects/project/global/sslCertificates/certificate_name'] 

['sstcloud.tagmate.app', 'deeptest.com', 'sst.tatvic.net', 'interntest.com', 'testtest.com']
