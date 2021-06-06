import { Component, Input, OnInit } from '@angular/core';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ImageUploaderOptions, FileQueueObject } from 'ngx-image-uploader-next';
import { UploaderDataService } from 'src/app/core/state/uploader/uploader-data.service';
@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.scss']
})
export class UploaderComponent implements OnInit {
  selectedFiles: FileList;
  progressInfos = [];
  message = '';

  fileInfos: Observable<any>;

  // options: ImageUploaderOptions = {
  //   thumbnailHeight: 400,
  //   thumbnailWidth: 1150,
  //   uploadUrl: 'http://some-server.com/upload',
  //   allowedImageTypes: ['image/png', 'image/jpeg'],
  // };


  constructor(private uploadService: UploaderDataService) { }

  ngOnInit(): void {
    this.fileInfos = this.uploadService.getFiles();
  }


  onUpload(file: FileQueueObject) {
    console.log(file.response);
  }

  selectFiles(e): void {
    this.progressInfos = [];
    this.selectedFiles = e.target.files;
  }

  uploadFiles(): void {
    this.message = '';

    for (let i = 0; i < this.selectedFiles.length; i++) {
      this.upload(i, this.selectedFiles[i]);
    }
  }

  upload(idx, file): void {
    this.progressInfos[idx] = { value: 0, fileName: file.name };

    this.uploadService.upload(file).subscribe(
      event => {
        if (event.type === HttpEventType.UploadProgress) {
          this.progressInfos[idx].value = Math.round(100 * event.loaded / event.total);
        } else if (event instanceof HttpResponse) {
          this.fileInfos = this.uploadService.getFiles();
        }
      },
      err => {
        this.progressInfos[idx].value = 0;
        this.message = 'Could not upload the file:' + file.name;
      });
  }
}
