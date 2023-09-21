import { AfterViewInit, Component, ElementRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-main-menu',
  templateUrl: './main-menu.component.html',
  styleUrls: ['./main-menu.component.css']
})
export class MainMenuComponent implements AfterViewInit,OnInit {

  constructor(private elementRef: ElementRef,private router: Router) { }
  goToGameMenu():void{
    this.router.navigate(["gameMenu"])
  }
  ngOnInit(): void {
  }
  ngAfterViewInit(): void {
    this.elementRef.nativeElement.ownerDocument
            .body.style.backgroundColor = '#EEA47F';
  }

}
