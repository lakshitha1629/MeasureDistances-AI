import { Injectable } from '@angular/core';
import { NgEntityService, NgEntityServiceConfig } from '@datorama/akita-ng-entity-service';
import { Uploader } from './uploader.model';
import { UploaderStore, UploaderState } from './uploader.store';

@Injectable({ providedIn: 'root' })
export class UploaderService extends NgEntityService<UploaderState> {

  constructor(protected store: UploaderStore) {
    super(store);
  }

  setItems(uploader: Uploader[]) {
    this.store.set(uploader);
  }

}
