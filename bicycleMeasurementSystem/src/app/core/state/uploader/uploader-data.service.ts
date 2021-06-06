import { HttpClient, HttpEvent, HttpRequest } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "src/environments/environment";
@Injectable({ providedIn: 'root' })
export class UploaderDataService {

  constructor(private httpClient: HttpClient) {
  }

  upload(file: File): Observable<HttpEvent<any>> {
    const formData: FormData = new FormData();
    formData.append('file', file);
    const request = new HttpRequest('POST', `${environment.apiUrl}getRatio`, formData, {
      reportProgress: true,
      responseType: 'json'
    });

    return this.httpClient.request(request);
  }

  getFiles(): Observable<any> {
    return this.httpClient.get(`${environment.apiUrl}getRatio`);
  }

}
