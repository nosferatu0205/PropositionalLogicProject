export class Board{
    size  : number = 10;
    private boardMatrix : number[][] = [];  
    
    constructor(boardSize : number) { 
        this.size = boardSize;
		for (var i = 0; i < this.size; i++) {
			this.boardMatrix[i] = Array(this.size).fill(0);
		}
    }
	public clone(): Board {
        let cloneBoard = new Board(this.size);
		for(let i=0;i<this.size;i++){
			for(let j=0;j<this.size;j++){
				cloneBoard.boardMatrix[i][j]=this.boardMatrix[i][j];
			}
		}
		return cloneBoard;
    }

	public getBoardValue(x:number,y:number) : number{
		return this.boardMatrix[x][y];
	}

    public getBoardSize() : number{
		return this.size;
	}

    public setBoardSize(size : number){
		this.size = size;
	}

    public getBoardMatrix() : number[][]{
		return this.boardMatrix;
	}
	


 

}