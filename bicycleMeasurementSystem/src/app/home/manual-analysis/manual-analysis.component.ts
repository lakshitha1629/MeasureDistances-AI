

import { HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { UploaderDataService } from 'src/app/core/state/uploader/uploader-data.service';
import { fromEvent, Observable } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
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
  @ViewChild('canvasInput')
  canvasInput: ElementRef;
  // @ViewChild('canvasOutput')
  // canvasOutput: ElementRef;

  constructor(private ngOpenCVService: NgOpenCVService,
    private uploadService: UploaderDataService,
    private uploaderService: UploaderService,
    private uploaderQuery: UploaderQuery) {

  }

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
            return this.ngOpenCVService.loadImageToHTMLCanvas(`${reader.result}`, this.canvasInput.nativeElement);
          }),
          tap(() => {
            let srcImg = cv.imread(this.canvasInput.nativeElement.id);
            let dst = new cv.Mat();
            let dsize = new cv.Size(500, 500);
            cv.resize(srcImg, dst, dsize, 0, 0, cv.INTER_AREA);
            cv.imshow(<HTMLCanvasElement>document.getElementById('canvasOutput'), dst);
            srcImg.delete();
            dst.delete();

            const canvas = <HTMLCanvasElement>document.getElementById('canvasOutput');
            canvas.addEventListener("click", drawLine, false);

            var clicks = 0;
            var lastClick = [0, 0];
            var x;
            var y;

            function getCursorPosition(e) {
              if (e.pageX != undefined && e.pageY != undefined) {
                x = e.pageX;
                y = e.pageY;
              } else {
                x =
                  e.clientX +
                  document.body.scrollLeft +
                  document.documentElement.scrollLeft;
                y =
                  e.clientY +
                  document.body.scrollTop +
                  document.documentElement.scrollTop;
              }

              return [x, y];
            }

            function drawLine(e) {
              var canvas = <HTMLCanvasElement>document.getElementById('canvasOutput'),
                context = this.getContext('2d');
              // const canvads = <HTMLCanvasElement>document.getElementById('canvasOutput');
              // const context = canvads.getContext("2d");
              // // let context = this.getContext("2d");
              // console.log(context);

              // context.beginPath();
              // context.moveTo(50, 50);
              // context.lineTo(250, 150);
              // context.stroke();

              x = getCursorPosition(e)[0] - this.offsetLeft;
              y = getCursorPosition(e)[1] - this.offsetTop;

              if (clicks != 1) {
                clicks++;
              } else {
                context.beginPath();
                context.moveTo(lastClick[0], lastClick[1]);
                context.lineTo(x, y);

                context.strokeStyle = "#FF0000";
                context.stroke();

                clicks = 0;
              }

              lastClick = [x, y];
            }
          }),
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

