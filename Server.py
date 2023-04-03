import cgi
import os
import mimetypes
from http.server import SimpleHTTPRequestHandler, HTTPServer

class FileUploadRequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

        response = '''
        <!doctype html>
        <title>Upload a File</title>
        <h1>Upload a File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
        '''
        self.wfile.write(response.encode())

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST', 'CONTENT_TYPE': self.headers['Content-Type']}
        )

        if 'file' not in form:
            self.send_error(400, 'No file part')
            return

        file_item = form['file']

        if file_item.filename == '':
            self.send_error(400, 'No selected file')
            return

        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

        content_type, _ = mimetypes.guess_type(file_item.filename)

        if content_type and content_type.startswith('text/'):
            response = file_item.file.read().decode('utf-8')
        else:
            response = f"File name: {file_item.filename}\nFile size: {len(file_item.value)} bytes\nContent-Type: {content_type}"

        self.wfile.write(response.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, FileUploadRequestHandler)
    print('Serving on port 8000...')
    httpd.serve_forever()
