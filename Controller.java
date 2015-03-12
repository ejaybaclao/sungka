package game;


public class Controller implements java.awt.event.KeyListener, java.awt.event.MouseListener, java.awt.event.MouseMotionListener{

	Window w;
	Player p; 
	java.util.Vector<Enemy> e; 
	java.util.Vector<Shot> s; 
	javax.swing.JFrame f; 
	java.awt.Point mouse_pos; 
	int health; 
	int shaking; 
	int level; 
	int xp; 
	int levelup; 
	int score; 
	int cooldown; 
	int waittime; 
	boolean pause;
	
	Controller(javax.swing.JFrame f){
		mouse_pos = new java.awt.Point(0, 0); 
		w = new Window(this); 
		p = new Player(this); 
		e = new java.util.Vector<Enemy>(); 
		s = new java.util.Vector<Shot>(); 
		health = 450;
		shaking = 0;
		level = 1;
		xp = 0;
		levelup = 0;
		score = 0;
		cooldown = 0;
		waittime = 0;
		this.f = f; 
		this.f.getContentPane().add(w, java.awt.BorderLayout.CENTER);
		this.f.pack(); 
		this.f.addMouseListener(this); 
		this.f.addMouseMotionListener(this); 
		this.f.addKeyListener(this); 
		run(); }
	
	void run(){
		while(true){ 
			if(pause){
		
				w.repaint();
			
				try{
					Thread.sleep(100);
				}catch(Exception e){}
		
				continue;
			}
		
			if(cooldown > 0){
				cooldown--;
			}
			
			if(Math.random() < ((0.002*level*level)/10)+0.0001*waittime && !p.dead){ 
				e.add(new Enemy(this));
			
				waittime = 0;
				if(Math.random() < 0.66){
				
					e.get(e.size()-1).x = (Math.random() < 0.5? -50: 550);
					e.get(e.size()-1).y = (int)(Math.random()*400);
				}else{ //ellers
				
					e.get(e.size()-1).x = (int)(Math.random()*400);
					e.get(e.size()-1).y = -50;
				}
				e.get(e.size()-1).health = 5*level*level;
			}else{
			
				waittime++;
			}
			
			p.run();

			for(int i = 0; i < e.size(); i++){
		
				e.get(i).run();
			
				if(e.get(i).dead){
				
					if(e.get(i).y > 500){
					
						e.remove(i);
					
						i--;
					}
				}
			}
	
			for(int i = 0; i < s.size(); i++){
	
				s.get(i).run();
				
				if(s.get(i).x > 500 || s.get(i).y > 500 || s.get(i).x < 0 || s.get(i).y < 0){
					
					s.remove(i);
					
					i--;
				
				}else if(!s.get(i).friendly){
					
					int xdiff = (p.x+p.cox)-(s.get(i).x);
					int ydiff = (p.y+p.coy)-(s.get(i).y);
				
					if(Math.abs(xdiff) < 50 && Math.abs(ydiff) < 50){
					
						s.remove(i);
					
						i--;
						
						p.damage = 20;
					
						health -= 25;
					
						shaking = 20;
					
						if(health <= 0){
							
							p.dead = true;
							
							p.vy = -10;
							
							p.vx = 0;
						}
					}
				
				}else{
					
					for(int j = 0; j < e.size(); j++){
						
						if(!e.get(j).dead){
							
							int xdiff = (e.get(j).x+e.get(j).cox)-(s.get(i).x);
							int ydiff = (e.get(j).y+e.get(j).coy)-(s.get(i).y);
							
							if(Math.abs(xdiff) < 50 && Math.abs(ydiff) < 50){
								
								s.remove(i);
								
								i--;
								
								e.get(j).damage = 20;
								
								e.get(j).health -= 10;
								
								if(e.get(j).health <= 0){
									
									e.get(j).dead = true;
									
									e.get(j).vy = -10;
									
									score += 250*level;
									
									xp++;
									
									if(xp > level*6){
										
										xp -= level*6;
										
										level++;
										
										levelup = 150;
										
										score += 10000*level;
									}
								}
								
								break;
							}
						}
					}
				}
			}
			
			w.repaint();
			
			try{
				Thread.sleep(20);
			}catch(Exception e){}
		}
	}
	
	public void keyReleased(java.awt.event.KeyEvent e){
		
		if(!p.dead){
			
			if(e.getKeyCode() == 65 || e.getKeyCode() == 68){
				
				p.vx = 0;
			}
		}
	}
	
	public void keyPressed(java.awt.event.KeyEvent e){
		
		if(!p.dead){
			
			if(e.getKeyCode() == 65){
				
				p.vx = -4;
			
			}else if(e.getKeyCode() == 68){
				
				p.vx = 4;
			
			}else if(e.getKeyCode() == 32){
			
				if(p.y == 400-p.h){
				
					p.y -= 10;
				
					p.vy = -10;
				}

			}else if(e.getKeyCode() == 80){
				
				if(pause){
					pause = false;
				}else{
					pause = true;
				}
			}
		}
	}
	
	public void keyTyped(java.awt.event.KeyEvent e){}
	public void mouseExited(java.awt.event.MouseEvent e){}
	public void mouseEntered(java.awt.event.MouseEvent e){}
	public void mouseClicked(java.awt.event.MouseEvent e){}
	
	@SuppressWarnings("static-access")
	public void mouseReleased(java.awt.event.MouseEvent e){
		
		if(p.y > 2000){

			if(e.getButton() == e.BUTTON1){
				
				if(mouse_pos.x > 150 && mouse_pos.x < 350 && mouse_pos.y > 300 && mouse_pos.y < 350){
					
					System.exit(0);
				}
			}
		}
	}
	
	@SuppressWarnings("static-access")
	public void mousePressed(java.awt.event.MouseEvent e){

		if(!p.dead && !pause){
	
			if(e.getButton() == e.BUTTON1){

				int xdiff = mouse_pos.x-(p.x+p.cox);
				int ydiff = mouse_pos.y-(p.y+p.coy);
		
				double length = Math.sqrt(xdiff*xdiff+ydiff*ydiff);
			
				s.add(new Shot(p.x+p.cox, p.y+p.coy, (int)(xdiff*(5/length)), (int)(ydiff*(5/length)), true));
	
			}else if(e.getButton() == e.BUTTON3){
		
				if(cooldown == 0){
					
					for(int i = 0; i < 360; i += 360/40){
						s.add(new Shot(p.x+p.cox, p.y+p.coy, (int)(Math.cos(i)*10), (int)(Math.sin(i)*10), true));
					}
		
					cooldown = 450-level*15;
				}
			}
		}
	}

	public void mouseMoved(java.awt.event.MouseEvent e){
		
		mouse_pos.setLocation(e.getX(), e.getY());
	}
	
	public void mouseDragged(java.awt.event.MouseEvent e){
	
		mouse_pos.setLocation(e.getX(), e.getY());
	}
}
