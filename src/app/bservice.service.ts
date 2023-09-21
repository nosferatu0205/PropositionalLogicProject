import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class BserviceService {
  gameResult:any=3;
  public rand:any=false;
  wumpus={
    "x": 2,"y": 2
  };
  coin={
    "x": 3,"y": 3
  };
  agent={
    "x": 4,"y": 4
  }
  pit:any=[];

  getWumpus():any{
    return this.wumpus;
  };
  getCoin():any{
    return  this.coin;
  };
  getpit():any{
    return  this.pit;
  };
  getagent():any{
    return  this.agent;
  };
  setWumpus(wumpus:any){
    this.wumpus=wumpus;
  };
  setCoin(coin:any){
    this.coin=coin;
  };
  setpit(pit:any){
    this.pit=pit;
  };
  setagent(agent:any){
    this.agent=agent;
  };

  constructor() { }
}
