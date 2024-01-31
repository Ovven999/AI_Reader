import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatExpansionModule } from '@angular/material/expansion';
import {MatCardModule} from '@angular/material/card';
import {MatToolbarModule} from '@angular/material/toolbar';

import { AppComponent } from './app.component';
import { LyricsPlayerComponent } from './Lyrics/lyrics.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HeaderComponent } from './header/header.component';
import {MusicPlayerComponent} from './music_player/music_player.component'
import { AppRountingModule } from './app-routing.module';
import { MusicPlayerPhoneComponent } from './music_player_phone/music_player_phone.component';
import { ArtBoardComponent } from './art-board/art-board.component';
import { MusicPlayerFasterComponent } from './music_player_faster/music_player_faster.component';

@NgModule({
  declarations: [
    AppComponent,
    LyricsPlayerComponent,
    HeaderComponent,
    MusicPlayerComponent,
    MusicPlayerPhoneComponent,
    ArtBoardComponent,
    MusicPlayerFasterComponent
  ],
  imports: [
    BrowserModule,
    AppRountingModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    MatInputModule,
    MatButtonModule,
    MatExpansionModule,
    MatCardModule,
    ReactiveFormsModule,
    MatToolbarModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
