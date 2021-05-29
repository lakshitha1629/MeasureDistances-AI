import { Component, OnInit } from '@angular/core';
import { ImageUploaderOptions, FileQueueObject } from 'ngx-image-uploader-next';
@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.scss']
})
export class UploaderComponent implements OnInit {
  imageOptions: ImageUploaderOptions = {
    uploadUrl: 'https://fancy-image-uploader-demo.azurewebsites.net/api/demo/upload',
    cropEnabled: true,
    thumbnailResizeMode: 'fill',
    autoUpload: false,
    resizeOnLoad: false,
    thumbnailWidth: 1150,
    thumbnailHeight: 400
  };

  constructor() { }

  ngOnInit(): void {
  }
  // onUpload(file: FileQueueObject) {
  //   console.log(file.response);
  // }
}
