import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GameMenuuComponent } from './game-menuu.component';

describe('GameMenuuComponent', () => {
  let component: GameMenuuComponent;
  let fixture: ComponentFixture<GameMenuuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GameMenuuComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GameMenuuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
