import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { environment } from "src/environments/environment";

import { tap } from 'rxjs/operators';
import { Uploader } from "./uploader.model";
import { UploaderService } from "./uploader.service";
import { UploadRequest } from "src/app/model/upload-request.model";


@Injectable({ providedIn: 'root' })
export class UploaderDataService {

  constructor(private http: HttpClient, private uploaderService: UploaderService) {
  }

  getItems(uploadRequest: UploadRequest): Observable<Uploader[]> {
    const data = new FormData()
    return this.http.post<Uploader[]>(`${environment.apiUrl}getRatio`, uploadRequest).pipe(tap((items) => {
      this.uploaderService.setItems(items);
    }));
  }

}
