package game;



public class Player{
	
	public int x, y, w, h, cox, coy; 
	public double vx, vy; 
	java.awt.GradientPaint gp1; 
	java.awt.geom.Ellipse2D e1, e2, e3; 
	java.awt.geom.Rectangle2D r1; 
	java.awt.BasicStroke bs1; 
	java.awt.geom.Line2D l1, l2, l3, l4, l5, l6; 
	Controller parent; 
	int damage; 
	boolean dead; 
	
	public Player(Controller parent){
	
		x = 200;
		y = 100;
		w = 75;
		h = 75;
		cox = 30;
		coy = 45;
		damage = 0;
		
		this.parent = parent;

		gp1 = new java.awt.GradientPaint(x, y, new java.awt.Color(255, 200, 0), x, y+h, new java.awt.Color(255, 75, 0), true);
		e1 = new java.awt.geom.Ellipse2D.Double(0, 0, w, h);
		e2 = new java.awt.geom.Ellipse2D.Double(0, 0, 20, 30);
		e3 = new java.awt.geom.Ellipse2D.Double(0, 0, 8, 8);
		r1 = new java.awt.geom.Rectangle2D.Double(-25, -10, 75, 25);
		bs1 = new java.awt.BasicStroke(2);
		l1 = new java.awt.geom.Line2D.Double(0, 0, 40, 20);
		l2 = new java.awt.geom.Line2D.Double(0, 20, 40, 0);
		l3 = new java.awt.geom.Line2D.Double(0, 20, 20, 0);
		l4 = new java.awt.geom.Line2D.Double(0, 0, 20, 20);
		l5 = new java.awt.geom.Line2D.Double(20, 20, 40, 0);
		l6 = new java.awt.geom.Line2D.Double(20, 0, 40, 20);
	}
	
	public int target(int i){
		
		if(i == 0){
			
			return parent.mouse_pos.x;
		
		}else{
			
			return parent.mouse_pos.y;
		}
	}
	
	public void paint(java.awt.Graphics2D g){
		
		int tx = x, ty = y, tcox = cox, tcoy = coy;
		
		g.translate(tx, ty);
		
			g.setPaint(gp1);
		
			g.fill(e1);
		
			g.setStroke(bs1);
		
			g.setPaint(java.awt.Color.BLACK);
	
			g.draw(e1);
	
			g.translate(17, 10);
				
				if(dead){
					
					g.draw(l3);
					g.draw(l4);
					g.draw(l5);
					g.draw(l6);
				
				}else if(damage > 0){
					
					damage--;
					
					g.draw(l1);
					g.draw(l2);
				
				}else{
				
					g.setPaint(java.awt.Color.WHITE);
				
					g.fill(e2);
				
					g.setPaint(java.awt.Color.BLACK);
					
					g.draw(e2);
				
					g.translate(6, 10);
						
						g.fill(e3);
					
					g.translate(-6, -10);
				
					g.translate(22, 0);
					
						g.setPaint(java.awt.Color.WHITE);
						
						g.fill(e2);
						
						g.setPaint(java.awt.Color.BLACK);
						
						g.draw(e2);
					
						g.translate(6, 10);
							
							g.fill(e3);
				
						g.translate(-6, -10);
		
					g.translate(-22, 0);
				}
		
			g.translate(-17, -10);
			
			g.translate(tcox, tcoy);
			
				double xdiff = target(0)-(tx+tcox);
				double ydiff = target(1)-(ty+tcoy);
				
				if(ydiff != 0){
		
					g.rotate(Math.atan(ydiff/xdiff));
			
					if(xdiff < 0){
						
						g.rotate(Math.PI);
					}
				}
			
				g.setPaint(java.awt.Color.GRAY);
		
				g.fill(r1);
		
				g.setPaint(java.awt.Color.BLACK);
				
				g.draw(r1);
				
				if(ydiff != 0){
					g.rotate(-Math.atan(ydiff/xdiff));
					if(xdiff < 0){
						g.rotate(-Math.PI);
					}
				}
	
			g.translate(-tcox, -tcoy);
		
		g.translate(-tx, -ty);
	}

	public void run(){
		
		if(dead){
			
			vy += 0.2;
	
		}else{
	
			if(y+h < 400){
				
				vy += 0.2;
			
			}else if(y+h > 400){
			
				vy = 0;
			
				y = 400-h;
			}
		}

		x += Math.ceil(vx);
		y += Math.ceil(vy);
		
		if(x > 500-h){
		
			x = 500-h;
		
		}else if(x < 0){
			x = 0;
		}
	}
}
