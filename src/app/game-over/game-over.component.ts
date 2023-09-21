import { AfterViewChecked, AfterViewInit, Component, ElementRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BserviceService } from '../bservice.service';

@Component({
  selector: 'app-game-over',
  templateUrl: './game-over.component.html',
  styleUrls: ['./game-over.component.css']
})
export class GameOverComponent implements OnInit,AfterViewInit {
  sstr:string="";
  constructor(private elementRef: ElementRef,private router: Router,private srv: BserviceService) {
    if(this.srv.gameResult==1){
      this.sstr="Game Over";
    }
    else{
      this.sstr="You Win";
    }
   }
  ngAfterViewInit(): void {
    this.elementRef.nativeElement.ownerDocument
    .body.style.backgroundColor = "#EEA47F";
  }

  ngOnInit(): void {
  }
  MainMenu():void{
    this.router.navigate([""]);
  }
}
