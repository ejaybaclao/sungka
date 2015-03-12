package game;


public class Enemy extends Player{
	
	int health; 
	public Enemy(Controller parent){
		super(parent);
		
		gp1 = new java.awt.GradientPaint(x, y, new java.awt.Color(255, 50, 0), x, y+h, new java.awt.Color(150, 50, 0), true);
		
		x = 0;
		y = 0;
		health = 1;
	}
	
	public int target(int i){
		if(i == 0){
			
			return parent.p.x+parent.p.cox;
		}else{
		
			return parent.p.y+parent.p.coy;
		}
	}
	
	public void run(){
		
		if(dead){
			
			vy += 0.2;
			y += vy;
		
		}else{
			
			if(parent.p.dead){
				
				return;
			}
			
			int xdiff = (parent.p.x+parent.p.cox)-(x+cox);
			int ydiff = (parent.p.y+parent.p.coy)-(y+coy);
			
			if(xdiff > 0){
				
				x += 2;
		
			}else if(xdiff < 0){
				
				x -= 2;
			}
			
			if(ydiff > 0){
				
				y += 2;
			
			}else if(ydiff < 0){
				
				y -= 2;
			}
			
			if(Math.abs(xdiff) < 50 && Math.abs(ydiff) < 50){
				
				parent.health--;
				
				parent.shaking = 10;
				
				parent.p.damage = 10;
				
				if(parent.health <= 0){
					
					parent.p.dead = true;
					
					parent.p.vy = -10;
					
					parent.p.vx = 0;
				}
			}
			
			if(Math.random() < ((0.002*parent.level*parent.level)/10)+0.005 && !parent.p.dead){
			
				xdiff = (parent.p.x+parent.p.cox)-(x+cox);
				ydiff = (parent.p.y+parent.p.coy)-(y+coy);
				
				double length = Math.sqrt(xdiff*xdiff+ydiff*ydiff);
				
				parent.s.add(new Shot(x+cox, y+coy, (int)(xdiff*(5/length)), (int)(ydiff*(5/length)), false));
			}
		}
	}
}
