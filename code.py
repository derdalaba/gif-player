import mdns
import socketpool
import wifi

from adafruit_httpserver import Server, Request, FileResponse

wifi.radio.start_ap("esp","password")
print(wifi.radio.ipv4_address_ap)

mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "gif-uploader"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)

pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/web", debug=True)

print(server.host)

@server.route("/")
def base(request: Request):
    """
    Serve the default index.html file.
    """
    return FileResponse(request, "index.html")

@server.route("/", "POST")
def route_func(request):
    #get file upload
    #file = request.form_data.files.get("uploaded_file")
    print(request.form_data.files.get("uploaded_file").filename)
          

server.serve_forever(str(wifi.radio.ipv4_address_ap), port=80)
