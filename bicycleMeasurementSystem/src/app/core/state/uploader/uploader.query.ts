import { Injectable } from '@angular/core';
import { QueryEntity } from '@datorama/akita';
import { UploaderStore, UploaderState } from './uploader.store';

@Injectable({ providedIn: 'root' })
export class UploaderQuery extends QueryEntity<UploaderState> {

  constructor(protected store: UploaderStore) {
    super(store);
  }

}
