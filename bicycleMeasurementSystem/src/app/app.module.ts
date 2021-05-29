import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { NavComponent } from './nav/nav.component';
import { FooterComponent } from './footer/footer.component';
import { HomeComponent } from './home/home.component';
import { BannerComponent } from './home/banner/banner.component';
import { SelectTypeComponent } from './home/select-type/select-type.component';
import { UploaderComponent } from './home/uploader/uploader.component';
import { AboutComponent } from './about/about.component';

import { ImageUploaderModule } from 'ngx-image-uploader';

@NgModule({
  declarations: [
    AppComponent,
    NavComponent,
    FooterComponent,
    HomeComponent,
    BannerComponent,
    SelectTypeComponent,
    UploaderComponent,
    AboutComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    NgbModule,
    ImageUploaderModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
