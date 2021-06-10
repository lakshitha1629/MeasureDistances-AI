import { HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { UploaderDataService } from 'src/app/core/state/uploader/uploader-data.service';
import { fromEvent, Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { NgOpenCVService, OpenCVLoadResult } from 'ng-open-cv';
import { ImageUploaderOptions, FileQueueObject } from 'ngx-image-uploader-next';
import { UploaderService } from 'src/app/core/state/uploader/uploader.service';
import { Uploader } from 'src/app/core/state/uploader/uploader.model';
import { UploaderQuery } from 'src/app/core/state/uploader/uploader.query';

@Component({
  selector: 'app-manual-analysis',
  templateUrl: './manual-analysis.component.html',
  styleUrls: ['./manual-analysis.component.scss']
})
export class ManualAnalysisComponent implements OnInit {
  openCVLoadResult: Observable<OpenCVLoadResult>;
  uploaderItems$: Observable<Uploader[]>;
  uploaderItemsLength: number;
  selectedFiles: FileList;
  progressInfos = [];
  message: string;
  pixelRatio: Number;
  active: Number = 0;

  @ViewChild('fileInput')
  fileInput: ElementRef;
  @ViewChild('canvasOutput')
  canvasOutput: ElementRef;
  @ViewChild('canvas')
  canvas: ElementRef;

  constructor(private ngOpenCVService: NgOpenCVService, private uploadService: UploaderDataService, private uploaderService: UploaderService, private uploaderQuery: UploaderQuery) { }

  ngOnInit(): void {
    this.openCVLoadResult = this.ngOpenCVService.isReady$;
    // this.uploaderItems$ = this.uploaderQuery.selectAll().pipe(tap((uploaderItem) => {
    //   console.log(uploaderItem);
    //   this.uploaderItemsLength = uploaderItem.length;
    //   this.pixelRatio = uploaderItem[0].pixelRatio;

    // }));

    if (this.uploadService.getFiles()) {
      this.message = 'Active';
    } else {
      this.message = 'Inactive';
    }
  }


  onUpload(file: FileQueueObject) {
    console.log(file.response);
  }

  selectFiles(e): void {
    // image loaded to canvas
    if (e.target.files.length) {
      const reader = new FileReader();
      const load$ = fromEvent(reader, 'load');
      load$
        .pipe(
          switchMap(() => {
            return this.ngOpenCVService.loadImageToHTMLCanvas(`${reader.result}`, this.canvasOutput.nativeElement);
          })
        )
        .subscribe(
          () => { },
          err => {
            console.log('Error loading image', err);
          });
      reader.readAsDataURL(e.target.files[0]);
    }

    //init progress
    this.progressInfos = [];
    this.selectedFiles = e.target.files;
  }

  uploadFiles(): void {
    this.message = '';

    for (let i = 0; i < this.selectedFiles.length; i++) {
      this.upload(i, this.selectedFiles[i]);
    }
  }

  upload(idx, file) {
    this.progressInfos[idx] = { value: 0, fileName: file.name };
    this.uploadService.upload(file).subscribe(
      (res: HttpEvent<any>) => {

        if (res.type === HttpEventType.UploadProgress) {
          this.progressInfos[idx].value = Math.round(100 * res.loaded / res.total);
        }
        if (res.type === HttpEventType.Response) {
          console.log('Upload complete');
          console.log(res.body);
          this.pixelRatio = res.body.pixelRatio;
          this.active = 1;
          this.uploaderService.addUploaderItem({
            id: 1,
            pixelRatio: this.pixelRatio
          } as Uploader);
        }

      },
      (error) => {
        this.progressInfos[idx].value = 0;
        this.message = 'Could not upload the file:' + file.name;
        console.log(error);
      }
    )
  }

  resetProject() {
    this.uploaderService.deleteUploaderItem(1);
    console.log("Clear Uploader DB");

  }

}

