import { AfterContentInit, AfterViewInit, Component, ElementRef, HostListener, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { BserviceService } from '../bservice.service';
import { Board } from './board';
import { Pair } from './pair';
declare var require: any
var PriorityQueue = require('priorityqueuejs');

@Component({
  selector: 'app-board',
  templateUrl: './board.component.html',
  styleUrls: ['./board.component.css']
})
// 1: wumpus, 2:hole, 3:coin, 4:smell. 5: wind, 9: character
export class BoardComponent implements OnInit, AfterViewInit {

  constructor(private elementRef: ElementRef,private srv:BserviceService,private router: Router) {
    
		for (var i = 0; i < 10; i++) {
			this.boardMatrixStuff[i] = Array(10).fill(0);
      this.boardMatrixWall[i] = Array(10).fill(1);
      this.boardMatrixSmell[i] = Array(10).fill(0);
      this.boardMatrixWind[i] = Array(10).fill(0);
      let noParent = new Pair()
      noParent.First = -1
      noParent.Second = -1
      this.parent[i] = Array(10).fill(noParent);
		}
    if(this.srv.rand==true){
      this.generateCustom();
    }
    else{
      this.generate();
    }
    
   }
  generateCustom():void{
    this.currX=this.srv.getagent().x;
    this.currY=this.srv.getagent().y;
    this.boardMatrixWall[this.currX][this.currY]=0;
    this.boardMatrixStuff[this.srv.getWumpus().x][this.srv.getWumpus().y]=1;
    this.boardMatrixStuff[this.srv.getagent().x][this.srv.getagent().y]=9;
    this.boardMatrixStuff[this.srv.getCoin().x][this.srv.getCoin().y]=3;
    console.log(this.srv.getagent());
    for( let itr of this.srv.getpit()){
      this.boardMatrixStuff[itr.x][itr.y]=2;
    }
    this.processAdjacent();
  }
  generate():void{
    
    this.currX=Math.floor(Math.random()*10);
    console.log(this.currX)
    this.currY=Math.floor(Math.random()*10);
    this.boardMatrixStuff[this.currX][this.currY]=9;
    this.boardMatrixStuff[(this.currX+Math.floor(Math.random()*10))%10][(this.currX+Math.floor(Math.random()*10))%10]=1;
    this.boardMatrixStuff[(this.currX+Math.floor(Math.random()*10))%10][(this.currX+Math.floor(Math.random()*10))%10]=2;
    this.boardMatrixStuff[(this.currX+Math.floor(Math.random()*10))%10][(this.currX+Math.floor(Math.random()*10))%10]=2;
    this.boardMatrixStuff[(this.currX+Math.floor(Math.random()*10))%10][(this.currX+Math.floor(Math.random()*10))%10]=2;
    this.boardMatrixStuff[(this.currX+Math.floor(Math.random()*10))%10][(this.currX+Math.floor(Math.random()*10))%10]=3;

    this.boardMatrixWall[this.currX][this.currY]=0;
    this.processAdjacent();

  }

  compareNumbers = function(a : Pair, b : Pair) { 
    if(a.First.First==b.First.First) {
      return b.First.Second - a.First.Second;
    }
    return a.First.First - b.First.First; 
  };

  queue = new PriorityQueue(this.compareNumbers);

  wumpus:any=1;
  knowledgeBase:any[]=[];
  attack:any=0;
  coin:any=1;
  score:any=0;
  moveX:any[]=[0,1,-1,0];
  moveY:any[]=[1,0,0,-1];
  
  board : Board = new Board(10);
  boardMatrixStuff : any[][] = []; 
  boardMatrixWall : any[][] = []; 
  boardMatrixWind : any[][] = []; 
  boardMatrixSmell : any[][] = [];
  parent : any[][] = []; 
  iter: any = Array(100);
  key :any =null;
  currX: any=0;
  currY: any=0;
  stateString:any="ArrowDown";
  charState:string="../../assets/character/downidle.png";
  // coinPath:string="../../assets/character/coin.png";
  charStateList:any={"downIdle": "../../assets/character/downidle.png", 
  "leftIdle": "../../assets/character/leftidle.png",
  "upIdle": "../../assets/character/upidle.png",
  "rightIdle": "../../assets/character/rightidle.png"}

  ngOnInit(): void {

  }
  ngAfterViewInit(): void {
    this.elementRef.nativeElement.ownerDocument.body.style.backgroundColor="#EEA47F";
  }
  getWall(idx: number) : number{
    // console.log(idx);
    let xPos:number=Math.floor(idx/10);
    let yPos:number =idx%10;
  
    
    let retValue=this.boardMatrixWall[xPos][yPos];
    if(retValue==1){
      // console.log(retValue);
      // console.log("Index :  "+ idx);
      // console.log("X : "+ xPos);
      // console.log("Y : "+ yPos);
    }
    
    return retValue;

  }
  getStuff(idx: number) : number{
    // console.log(idx);
    let xPos:number=Math.floor(idx/10);
    let yPos:number =idx%10;
  
    
    let retValue=this.boardMatrixStuff[xPos][yPos];
    if(retValue==1){
      // console.log(retValue);
      // console.log("Index :  "+ idx);
      // console.log("X : "+ xPos);
      // console.log("Y : "+ yPos);
    }
    if(this.boardMatrixWall[xPos][yPos]!=0)return 0;
    return retValue;

  }
  getStuff2(idx: number) : number{
    // console.log(idx);
    let xPos:number=Math.floor(idx/10);
    let yPos:number =idx%10;
  
    
    let retValue=this.boardMatrixStuff[xPos][yPos];
    if(retValue==1){
      // console.log(retValue);
      // console.log("Index :  "+ idx);
      // console.log("X : "+ xPos);
      // console.log("Y : "+ yPos);
    }
    return retValue;

  }
  @HostListener('window:keydown.ArrowLeft', ['$event'])
  @HostListener('window:keydown.ArrowRight', ['$event'])
  @HostListener('window:keydown.ArrowUp', ['$event'])
  @HostListener('window:keydown.ArrowDown', ['$event'])
  @HostListener('window:keydown.Space',['$event'])
  @HostListener('window:keydown.Alt',['$event'])
  handleKeyboardEvent(event: KeyboardEvent) { 
    console.log(event.key);
    this.key = event.key;
    if(this.key=="Alt"){
      this.useAttack();
      console.log("herer");
      console.log( this.boardMatrixStuff[5][5]);
      console.log(this.stateString);
      return;
    }
    if(this.key!=this.stateString){
      this.stateString=this.key;
      if(this.key=="ArrowDown"){
        this.charState=this.charStateList["downIdle"];
      }
      if(this.key=="ArrowUp"){
        this.charState=this.charStateList["upIdle"];
      }
      if(this.key=="ArrowLeft"){
        this.charState=this.charStateList["leftIdle"];
      }
      if(this.key=="ArrowRight"){
        this.charState=this.charStateList["rightIdle"];
      }
    }
    else{
      if(this.key=="ArrowDown"){
        if(this.currX<9){
          this.movePlayer(this.currX,this.currY,this.currX+1,this.currY);
          this.currX+=1;
        }
         
      }
      if(this.key=="ArrowUp"){
        if(this.currX>0){
          this.movePlayer(this.currX,this.currY,this.currX-1,this.currY);
          this.currX-=1;
        }
      }
      if(this.key=="ArrowLeft"){
        if(this.currY>0){
          this.movePlayer(this.currX,this.currY,this.currX,this.currY-1);
          this.currY-=1;
        }
      }
      if(this.key=="ArrowRight"){
        if(this.currY<9){
          this.movePlayer(this.currX,this.currY,this.currX,this.currY+1);
          this.currY+=1;
        }
      }
      if(this.key==" "){
        console.log(this.key);
        let source = new Pair()
        source.First = this.currX
        source.Second = this.currY
        console.log("source", source)
        if(this.coin==0 && this.currX==0 && this.currY==0){
          this.currX = -1
          this.currY = -1
          this.srv.gameResult=0;
          this.router.navigate(["gameover"]);
        }
        else{
          this.bfs(source)
          let nextNode:Pair = this.bestMove().Second
          //let containsWumpus = (this.bestMove().First.First==1)
          console.log(nextNode.Second)
          //this.movePlayer(source.First, source.Second, nextNode.First, nextNode.Second)
          // this.travel(nextNode, containsWumpus)
          this.travel(nextNode)
          console.log(this.currX, this.currY)
        }
      }
     this.attack=Math.max(0,Math.floor(this.score/10));
    
  }
    // console.log("pos: "+ this.currX);
    // console.log("pos: "+ this.currY);
  }
  movePlayer(x1:any,y1:any,x2:any,y2:any):void{
    this.boardMatrixStuff[x1][y1]=0;
    this.boardMatrixWall[x2][y2]=0;
    if(this.boardMatrixStuff[x2][y2]==1){
      this.boardMatrixStuff[x2][y2]=0;
      this.currX=-1;
      this.currY=-1;
      this.srv.gameResult=1;
      this.router.navigate(["gameover"]);
    }
    else if(this.boardMatrixStuff[x2][y2]==2){
      this.boardMatrixStuff[x2][y2]=0;
      this.currX=-1;
      this.currY=-1;
      this.srv.gameResult=1;
      this.router.navigate(["gameover"]);
    }

    else if(this.boardMatrixStuff[x2][y2]==3){
      this.score+=1000;
      this.boardMatrixStuff[x2][y2]=0;
      this.coin--;
    }
    else{
      this.boardMatrixStuff[x2][y2]=9;
    }
    this.score-=1;
  }
  processMove():void{

  }
  processAdjacent():void{
    for(let i=0;i<10;i++){
      for(let j=0;j<10;j++){
        
        this.updateAdjacent(i,j,this.boardMatrixStuff[i][j]);
        
      }
    }
  }
  updateAdjacent(x:any, y:any,type:any):void{
    for(let i=0;i<4;i++){
      let newX=x+this.moveX[i];
      let newY=y+this.moveY[i];
      if(Math.min(newX,newY)>=0 && newX<10 && newY<10){
        if(type==1){
          this.boardMatrixSmell[newX][newY]=1;
        }
        if(type==2){
          this.boardMatrixWind[newX][newY]=1;
        }
      }
    }
    
  }
  useAttack():void{
    this.score=this.score-10;
    if(this.stateString=="ArrowRight"){
      for(let i=this.currY+1;i<10;i++){
        if(this.boardMatrixStuff[this.currX][i]==1){
          this.wumpus=0;
          this.score+=1000;
          this.boardMatrixStuff[this.currX][i]=0;
          this.cleanSmell(this.currX,i);
        }
      }
    }

    else if(this.stateString=="ArrowLeft"){
      for(let i=this.currY-1;i>=0;i--){
        if(this.boardMatrixStuff[this.currX][i]==1){
          this.wumpus=0;
          this.score+=1000;
          this.boardMatrixStuff[this.currX][i]=0;
          this.cleanSmell(this.currX,i);

        }
      }
    }

    else if(this.stateString=="ArrowDown"){
      for(let i=this.currX+1;i<10;i++){
        if(this.boardMatrixStuff[i][this.currY]==1){
          this.wumpus=0;
          this.score+=1000;
          this.boardMatrixStuff[i][this.currY]=0;
          this.cleanSmell(i,this.currY);

        }
      }
    }

    else if(this.stateString=="ArrowUp"){
      for(let i=this.currX-1;i>=0;i--){
        if(this.boardMatrixStuff[i][this.currY]==1){
          this.wumpus=0;
          this.score+=1000;
          this.boardMatrixStuff[i][this.currY]=0;
          this.cleanSmell(i,this.currY);

        }
      }
    }
    this.attack=Math.max(0,Math.floor(this.score/10));
  }
  cleanSmell(x:any, y:any):void{
    for(let i=0;i<4;i++){
      let newX=x+this.moveX[i];
      let newY=y+this.moveY[i];
      if(Math.min(newX,newY)>=0 && newX<10 && newY<10){
        this.boardMatrixSmell[newX][newY]=this.boardMatrixSmell[newX][newY]-1;
        //console.log(this.boardMatrixSmell[newX][newY]);
      }
    }
  }
  
  bfs(source : any){
    let visited: boolean[][] = [];
    //var size = this.board.getBoardSize();
    var size = 10;
    // Pre-populate array:
    this.parent = new Array<any>()
    this.knowledgeBase = new Array<any>()
    for(let i = 0; i < size; i++){
      visited[i] = Array(size).fill(false);
      let noParent = new Pair()
      noParent.First = -1
      noParent.Second = -1
      this.parent[i] = Array(10).fill(noParent);
    }

     // Use an array as our queue representation:
     let q: Pair[] = [];
     let sourceX = source.First
     let sourceY = source.Second
     visited[sourceX][sourceY] = true;
     
     let source_cost = new Pair()
     source_cost.First = source
     source_cost.Second = 0
     q.push(source_cost);

     while(q.length > 0){
         const v = q.shift();
         if(v?.First.First<0 || v?.First.First>=10 || v?.First.Second<0 || v?.First.Second>=10) continue
         console.log(v?.First.First, v?.First.First)
         for(let i=0; i<4; i++){
              
              let x = this.moveX[i]
              let y = this.moveY[i]
              let adjX = v?.First.First+x
              let adjY = v?.First.Second+y
              if(adjX<0 || adjY<0 || adjX>=10 || adjY>=10) continue
              
              let newNode = new Pair()
              newNode.First = adjX
              newNode.Second = adjY
              
              let cost = v?.Second+1                
              let risk_score = this.getScore(adjX, adjY)


              let score_cost = new Pair()
              score_cost.First = risk_score
              score_cost.Second = cost

              if(visited[adjX][adjY] == false){
                  visited[adjX][adjY] = true;

                  this.parent[adjX][adjY] = v?.First
                  if(this.boardMatrixWall[adjX][adjY] == 1){
                    console.log(adjX, adjY)
                    let score_cost_vertex = new Pair()
                    score_cost_vertex.First = score_cost
                    score_cost_vertex.Second = newNode
                    this.queue.enq(score_cost_vertex)
                    continue
                  }
                  let toAdd = new Pair()
                  toAdd.First = newNode
                  toAdd.Second = cost
                  q.push(toAdd);
              }
         }
     }
}

bestMove(): Pair{
  while(!this.queue.isEmpty()){
    let ret =  this.queue.deq();
    ret.First.First = Math.abs(ret.First.First)
    this.knowledgeBase.push(ret)
  }
  return this.knowledgeBase[0];
}

getScore(x : number, y:number) : number{
  let score = 0
  for(let i=0; i<4; i++){
    let adjX = x + this.moveX[i]
    let adjY = y + this.moveY[i]
    if(adjX<0 || adjY<0 || adjX>=10 || adjY>=10){
      continue
    }
    if(this.boardMatrixWall[adjX][adjY]==1) {
      score+=5
      continue
    }

    if(this.boardMatrixSmell[adjX][adjY]==0 && this.boardMatrixWind[adjX][adjY]==0){
      return 0;
    } 

    if(this.boardMatrixSmell[adjX][adjY]==1){
      let count = 0
      for(let j=0; j<4; j++){
        let X = adjX + this.moveX[j]
        let Y = adjY + this.moveY[j]
        if(X==x && Y==y) continue
        if(X<0 || Y<0 || X>=10 || Y>=10){
          continue
        }
        if(this.boardMatrixWall[X][Y]!=0) count += 1
      }
      // if(count==3) return 1;
      if(count==3) score += 100
      else score += 10
    }
    
    if(adjX<0 || adjY<0 || adjX>=10 || adjY>=10){
      continue
    }
    if(this.boardMatrixWind[adjX][adjY]==1){
      let count = 0
      for(let j=0; j<4; j++){
        let X = adjX + this.moveX[j]
        let Y = adjY + this.moveY[j]
        if(X==x && Y==y) continue
        if(X<0 || Y<0 || X>=10 || Y>=10){
          continue
        }
        if(this.boardMatrixWall[X][Y]!=0) count += 1
      }
      if(count==3) score += 100
      else score += 10
    }

  }
  return -score
}

travel(dest : Pair){
  let source : Pair = new Pair()
  source.First = this.currX
  source.Second = this.currY
  console.log(source, dest)
  var path : Pair[] = []
  var cur = dest
  path.push(cur)
  console.log("Rev : ", cur)
  //console.log(path)
  while(1){
    //count++
    cur = this.parent[cur.First][cur.Second]
    console.log(cur)
    path.push(cur)
    //console.log(path)
    if(cur.First==source.First && cur.Second==source.Second) break
  }
  path.reverse()
  
  for(let i=1; i<path.length; i++){
      this.movePlayer(this.currX, this.currY, path[i].First, path[i].Second)
      this.currX = path[i].First
      this.currY = path[i].Second
      // if(i==path.length-2){
      //   let dir = 0
      //   if(this.currX!=path[i+1].First){
      //     let dir = path[i+1].First - this.currX
      //     if(dir == -1){
      //       this.stateString = "ArrowLeft"
      //     }
      //     else{
      //       this.stateString = "ArrowRight"
      //     }
      //   }
      //   else {
      //     let dir = path[i+1].Second - this.currY
      //     if(dir == -1){
      //       this.stateString = "ArrowUp"
      //     }
      //     else{
      //       this.stateString = "ArrowDown"
      //     }
      //   }
      // }
      console.log("Currently at", cur.First, cur.Second)
  }
  
  console.log(path)
  
}

  getFeeling(idx:number):number{
    let xPos:number=Math.floor(idx/10);
    let yPos:number =idx%10;
  
    
    let smell=0;
    smell=this.boardMatrixSmell[xPos][yPos];
    let wind=0
    wind=this.boardMatrixWind[xPos][yPos];
    let total= wind+smell;
    let retValue:number=0;
    if(total==2){
      retValue= 3;
    }
    else if(smell==1){
      retValue=1;
    }
    else if(wind==1){
      retValue= 2;
    }
    if(this.boardMatrixWall[xPos][yPos]==1)return 0;
    if(this.boardMatrixStuff[xPos][yPos]!=0)return 0;
    return retValue;
  }
  getFeeling2(idx:number):number{
    let xPos:number=Math.floor(idx/10);
    let yPos:number =idx%10;
  
    
    let smell=0;
    smell=this.boardMatrixSmell[xPos][yPos];
    let wind=0
    wind=this.boardMatrixWind[xPos][yPos];
    let total= wind+smell;
    let retValue:number=0;
    if(total==2){
      retValue= 3;
    }
    else if(smell==1){
      retValue=1;
    }
    else if(wind==1){
      retValue= 2;
    }
    if(this.boardMatrixStuff[xPos][yPos]!=0)return 0;

    return retValue;
    
  }


}






