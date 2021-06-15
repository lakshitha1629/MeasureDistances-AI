import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class DataPassService {

  constructor() { }


  private newList = new BehaviorSubject<any>({
    flowerCenter: []
  });

  setData(data: any) {
    this.newList.next(data);
  }

  getData() {
    return this.newList.asObservable();
  }

}
