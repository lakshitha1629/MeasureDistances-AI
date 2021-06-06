import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MlAnalysisComponent } from './ml-analysis.component';

describe('MlAnalysisComponent', () => {
  let component: MlAnalysisComponent;
  let fixture: ComponentFixture<MlAnalysisComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MlAnalysisComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MlAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
