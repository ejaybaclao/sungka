package game;


public class Shot{

	public int x, y;
	double vx, vy; 
	boolean friendly;
	java.awt.geom.Ellipse2D e; 
	
	public Shot(int x, int y, int vx, int vy, boolean friendly){
	
		this.x = x;
		this.y = y;
		this.vx = vx;
		this.vy = vy;
		this.friendly = friendly;
	
		e = new java.awt.geom.Ellipse2D.Double(-8, -8, 16, 16);
	}
	
	public void paint(java.awt.Graphics2D g){
		
		g.translate(x, y);
			
			if(friendly){
			
				g.setPaint(java.awt.Color.YELLOW);
			
			}else{
				
				g.setPaint(java.awt.Color.ORANGE);
			}
		
			g.fill(e);
	
		g.translate(-x, -y);
	}
	
	public void run(){
		
		x += vx;
		y += vy;
	}
}
