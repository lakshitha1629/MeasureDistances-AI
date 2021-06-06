import { Component, OnInit } from '@angular/core';
import { ImageUploaderOptions, FileQueueObject } from 'ngx-image-uploader-next';
@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.scss']
})
export class UploaderComponent implements OnInit {
  options: ImageUploaderOptions = {
    thumbnailHeight: 400,
    thumbnailWidth: 1150,
    uploadUrl: 'http://some-server.com/upload',
    allowedImageTypes: ['image/png', 'image/jpeg'],
  };


  constructor() { }

  ngOnInit(): void {
  }

  onUpload(file: FileQueueObject) {
    console.log(file.response);
  }

}
