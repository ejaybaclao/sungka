package game;


public class Window extends javax.swing.JPanel{
	
	Controller parent; 
	java.awt.GradientPaint gp1, gp2; 
	java.awt.geom.Rectangle2D r1, r2, r3, r4; 
	java.awt.BasicStroke bs1; 
	java.awt.geom.Line2D s1, s2; 
	java.awt.Font f1, f2; 
	java.awt.geom.RoundRectangle2D rr1, rr2; 

	public Window(Controller c){
	
		parent = c;
		
		setPreferredSize(new java.awt.Dimension(500, 500));
		
		gp1 = new java.awt.GradientPaint(0, 0, new java.awt.Color(50, 200, 255), 0, 400, java.awt.Color.BLUE);
	
		gp2 = new java.awt.GradientPaint(0, 100, new java.awt.Color(150, 255, 150), 0, 500, new java.awt.Color(50, 200, 50));
	
		r1 = new java.awt.geom.Rectangle2D.Double(0, 0, 500, 400);
	
		r2 = new java.awt.geom.Rectangle2D.Double(0, 400, 500, 100);
	
		r3 = new java.awt.geom.Rectangle2D.Double(0, 0, 450, 50);

		r4 = new java.awt.geom.Rectangle2D.Double(0, 0, 450, 5);
	
		bs1 = new java.awt.BasicStroke(1);

		s1 = new java.awt.geom.Line2D.Double(-16, 0, 16, 0);
		s2 = new java.awt.geom.Line2D.Double(0, -16, 0, 16);
		
		f1 = new java.awt.Font("Arial", 0, 40);
		f2 = new java.awt.Font("Arial", 0, 20);
		
		rr1 = new java.awt.geom.RoundRectangle2D.Double(100, 100, 300, 300, 10, 10);
		rr2 = new java.awt.geom.RoundRectangle2D.Double(150, 300, 200, 50, 10, 10);
	}
	
	public void paint(java.awt.Graphics g){
		update(g);
	}
	
	public void update(java.awt.Graphics g2){
		
		java.awt.Graphics2D g = (java.awt.Graphics2D) g2;
		
		g.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);
		
		if(parent.shaking > 0){
		
			parent.shaking--;
			
			g.translate(Math.random()*5, Math.random()*5);
		}
		
		g.setPaint(gp1);
		
		g.fill(r1);
		
		g.setPaint(gp2);
		
		g.fill(r2);
		
		for(int i = 0; i < parent.e.size(); i++){
		
			parent.e.get(i).paint(g);
		}
		
		parent.p.paint(g);
		
		for(int i = 0; i < parent.s.size(); i++){
		
			parent.s.get(i).paint(g);
		}

		if(!parent.p.dead){
			
			g.translate(25, 25);
				
				r3.setRect(0, 0, parent.health, 25);
				
				if(parent.health > 225){
					
					g.setPaint(java.awt.Color.GREEN);
				
				}else if(parent.health > 100){
					
					g.setPaint(java.awt.Color.YELLOW);
				
				}else{
					
					g.setPaint(java.awt.Color.RED);
				}
			
				g.fill(r3);
	
				g.setPaint(java.awt.Color.BLACK);
			
				g.draw(r3);
			
				if(parent.cooldown > 0){
			
					g.translate(0, 25);
				
						g.setPaint(java.awt.Color.RED);
			
						r4.setRect(0, 0, parent.cooldown, 5);
				
						g.fill(r4);
				
						g.setPaint(java.awt.Color.BLACK);
			
						g.draw(r4);
	
					g.translate(0, -25);
				}
			
				g.translate(225, 33);
				
					g.setFont(f2);
				
					java.awt.FontMetrics fm = g.getFontMetrics();
				
					g.drawString("Score: "+parent.score+"   Level: "+parent.level, -fm.stringWidth("Score: "+parent.score+" : Level: "+parent.level)/2, -fm.getHeight()/2);
		
				g.translate(-225, -37);
	
			g.translate(-25, -25);
		}

		if(parent.levelup > 0){
		
			double rot = (Math.random()-0.5)/3;
		
			if(parent.levelup < 50){
		
				g.translate(250, 250-(-parent.levelup+50)*5);
			}else{
		
				g.translate(250, 250);
			}

			g.setFont(f1);
		
			java.awt.FontMetrics fm = g.getFontMetrics();
		
			g.rotate(rot);

				g.drawString("LEVEL UP", -fm.stringWidth("LEVEL UP")/2, -fm.getHeight());

			g.rotate(-rot);
		
			if(parent.levelup < 50){
				g.translate(-250, -(250-(-parent.levelup+50)*5));
			}else{
				g.translate(-250, -250);
			}
	
			parent.levelup--;
		}

		if(parent.p.y > 2000){
		
			parent.p.vy = 0;
	
			parent.p.y = 2001;
		
			g.setPaint(java.awt.Color.WHITE);

			g.fill(rr1);
		
			g.setPaint(java.awt.Color.BLACK);
		
			g.draw(rr1);
		
			g.setFont(f1);
	
			java.awt.FontMetrics fm = g.getFontMetrics();
		
			g.drawString("GAME OVER!", 250-fm.stringWidth("GAME OVER!")/2, 175-fm.getHeight()/2);
			
			g.drawString(""+parent.score, 250-fm.stringWidth(""+parent.score)/2, 275-fm.getHeight()/2);
			
			g.setFont(f2);
			
			fm = g.getFontMetrics();
		
			g.drawString("Final Score:", 250-fm.stringWidth("final Score:")/2, 220-fm.getHeight()/2);
			
			g.drawString("Quit", 250-fm.stringWidth("Quit")/2, 345-fm.getHeight()/2);
		
			g.draw(rr2);
		}
		
		if(parent.pause){
			
			g.setPaint(java.awt.Color.WHITE);
	
			g.fill(rr2);
		
			g.setPaint(java.awt.Color.BLACK);
	
			g.draw(rr2);
	
			g.setFont(f2);
	
			java.awt.FontMetrics fm = g.getFontMetrics();
			
			g.drawString("Pause", 250-fm.stringWidth("Pause")/2, 345-fm.getHeight()/2);
		}
		
		g.translate(parent.mouse_pos.x, parent.mouse_pos.y);
	
		g.setStroke(bs1);

		g.setPaint(java.awt.Color.BLACK);

		g.draw(s1);
		g.draw(s2);
	}
}
