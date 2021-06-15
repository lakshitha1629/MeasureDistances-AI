import { OnInit } from '@angular/core';
import { Flower } from '../models/flower';
import { Point } from '../models/point';
import { DataPassService } from '../services/data-pass.service';
import { FlowerRandomizationService } from '../services/flower-randomization.service';

export class InteractiveFlowers {
  private readonly context: CanvasRenderingContext2D;
  private readonly canvasWidth: number;
  private readonly canvasHeight: number;
  private flowers: Flower[] = [];
  private list: any[];
  private readonly randomizationService = new FlowerRandomizationService();
  private ctrlIsPressed = false;
  private mousePosition = new Point(-100, -100);

  constructor(private readonly canvas: HTMLCanvasElement, private dataService: DataPassService) {
    this.context = this.canvas.getContext('2d');
    this.canvasWidth = this.canvas.width;
    this.canvasHeight = this.canvas.height;

    this.addInteractions();
  }

  clearCanvas() {
    this.flowers = [];
    this.context.clearRect(0, 0, this.canvasWidth, this.canvasHeight);
  }

  addInteractions() {
    this.canvas.addEventListener('click', e => {
      if (this.ctrlIsPressed) {
        this.clearCanvas();
        return;
      }
      this.calculateMouseRelativePositionInCanvas(e);
      const flower = this.randomizationService.getFlowerAt(this.mousePosition);
      this.flowers.push(flower);
      this.list = this.flowers;
      const data = new DataPassService;
      // data.setData(this.flowers);
      console.log("setted");
      this.dataService.setData({
        flowerCenter: this.flowers
      });
    });



    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if (e.which === 17 || e.keyCode === 17) {
        this.ctrlIsPressed = true;
      }
    });
    window.addEventListener('keyup', () => {
      this.ctrlIsPressed = false;
    });
  }



  private calculateMouseRelativePositionInCanvas(e: MouseEvent) {
    this.mousePosition = new Point(
      e.clientX +
      (document.documentElement.scrollLeft || document.body.scrollLeft) -
      this.canvas.offsetLeft,
      e.clientY +
      (document.documentElement.scrollTop || document.body.scrollTop) -
      this.canvas.offsetTop
    );
    // console.log(this.mousePosition);
  }

  // someFunction(data) {
  //   this.dataPassService.setData(data);
  // }
}
