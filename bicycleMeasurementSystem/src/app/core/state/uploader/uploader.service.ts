import { Injectable } from '@angular/core';
import { NgEntityService, NgEntityServiceConfig } from '@datorama/akita-ng-entity-service';
import { UploaderStore, UploaderState } from './uploader.store';

@NgEntityServiceConfig({
  resourceName: 'getRatio',
})
@Injectable({ providedIn: 'root' })
export class UploaderService extends NgEntityService<UploaderState> {

  constructor(protected store: UploaderStore) {
    super(store);
  }

}
