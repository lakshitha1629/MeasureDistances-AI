import { HttpEvent, HttpEventType, HttpResponse } from '@angular/common/http';
import { Component, ElementRef, OnInit, ViewChild } from '@angular/core';
import { UploaderDataService } from 'src/app/core/state/uploader/uploader-data.service';
import { fromEvent, Observable } from 'rxjs';
import { switchMap, tap } from 'rxjs/operators';
import { NgOpenCVService, OpenCVLoadResult } from 'ng-open-cv';
import { UploaderService } from 'src/app/core/state/uploader/uploader.service';
import { Uploader } from 'src/app/core/state/uploader/uploader.model';
import { InteractiveFlowers } from './analysis/animations/interactive-flowers';
import { DataPassService } from './analysis/services/data-pass.service';

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
  pixelRatio: any = 0;
  active: Number = 0;
  pointCount: Number;
  imgWidth: number = 0;
  imgHeight: number = 0;
  saddleHeight: any = 0;
  reach: any = 0;

  @ViewChild('fileInput')
  fileInput: ElementRef;
  @ViewChild('canvasInput')
  canvasInput: ElementRef;
  @ViewChild('canvas')
  canvas: ElementRef;

  constructor(private ngOpenCVService: NgOpenCVService,
    private uploadService: UploaderDataService,
    private uploaderService: UploaderService,
    private dataPassService: DataPassService) {
  }

  ngOnInit(): void {
    this.openCVLoadResult = this.ngOpenCVService.isReady$;
    if (this.uploadService.getFiles()) {
      this.message = 'Active';
    } else {
      this.message = 'Inactive';
    }
    this.getFinalOutput();
  }

  getFinalOutput() {
    this.dataPassService.getData().subscribe(info => {
      console.log(info);
      this.pointCount = info.flowerCenter.length;

      if (this.pointCount == 2) {
        const xValuePoint1 = info.flowerCenter[0].flowerCenter.centerPoint.x;
        const yValuePoint1 = info.flowerCenter[0].flowerCenter.centerPoint.y;
        const xValuePoint2 = info.flowerCenter[1].flowerCenter.centerPoint.x;
        const yValuePoint2 = info.flowerCenter[1].flowerCenter.centerPoint.y;
        const Ratio1 = this.pixelRatio;
        console.log(Ratio1);
        const saddleHeight = ((((xValuePoint1 - xValuePoint2) * (this.imgWidth / 500)) + ((yValuePoint1 - yValuePoint2) * (this.imgHeight / 500))) * Ratio1).toFixed(2);
        // this.saddleHeight = (Math.abs(parseFloat(saddleHeight)) / 10).toFixed(2);
        this.saddleHeight = (((xValuePoint1 - xValuePoint2) + (yValuePoint1 - yValuePoint2)) * Ratio1).toFixed(2);

      }

      if (this.pointCount == 4) {
        const xValuePoint3 = info.flowerCenter[2].flowerCenter.centerPoint.x;
        const yValuePoint3 = info.flowerCenter[2].flowerCenter.centerPoint.y;
        const xValuePoint4 = info.flowerCenter[3].flowerCenter.centerPoint.x;
        const yValuePoint4 = info.flowerCenter[3].flowerCenter.centerPoint.y;
        const Ratio2 = this.pixelRatio;
        console.log(Ratio2);
        const reach = ((((xValuePoint3 - xValuePoint4) * (this.imgWidth / 500)) + ((yValuePoint3 - yValuePoint4) * (this.imgHeight / 500))) * Ratio2).toFixed(2);
        console.log(this.reach);
        // this.reach = (Math.abs(parseFloat(reach)) / 10).toFixed(2);
        this.reach = (((xValuePoint3 - xValuePoint4) + (yValuePoint3 - yValuePoint4)) * Ratio2).toFixed(2);

      }

      if (this.pointCount == 5) {
        const canvas = <HTMLCanvasElement>document.getElementById('canvas');
        const flowers = new InteractiveFlowers(canvas, this.dataPassService);
        flowers.clearCanvas();
      }

    });
  }

  selectFiles(e): void {
    // image loaded to canvas
    if (e.target.files.length) {
      const reader = new FileReader();
      const load$ = fromEvent(reader, 'load');
      load$
        .pipe(
          switchMap(() => {
            return this.ngOpenCVService.loadImageToHTMLCanvas(`${reader.result}`, this.canvas.nativeElement);
          }),
          tap(() => {
            this.canvas.nativeElement.addEventListener("click", drawLine);
            var clicks = 0;
            var lastClick = [0, 0];

            function getCursorPosition(e) {
              var x;
              var y;

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
              // console.log(x, y);

              return [x, y];
            }

            function drawLine(e) {
              var x;
              var y;

              const context = this.getContext("2d");

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
          })
        )
        .subscribe(
          () => {
          },
          err => {
            console.log('Error loading image', err);
          });

      reader.readAsDataURL(e.target.files[0]);
      reader.onload = (e: any) => {
        var myImage = new Image();
        myImage.src = e.target.result;
        myImage.onload = function (ev: any) {
          let srcImg = cv.imread(myImage);
          console.log(srcImg);
          let dst = new cv.Mat();
          let dsize = new cv.Size(500, 500);
          cv.resize(srcImg, dst, dsize, 0, 0, cv.INTER_AREA);
          cv.imshow("canvas", dst);
          srcImg.delete();
          dst.delete();
        };
      }
      const canvas = <HTMLCanvasElement>document.getElementById('canvas');
      const flowers = new InteractiveFlowers(canvas, this.dataPassService);
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
          this.imgWidth = res.body.width;
          this.imgHeight = res.body.height;
          this.active = 1;
          this.uploaderService.addUploaderItem({
            id: 1,
            pixelRatio: this.pixelRatio,
            imgWidth: this.imgWidth,
            imgHeight: this.imgHeight
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

