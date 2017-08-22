 //Reference the required Java libraries
 import java.applet.Applet; 
 import java.awt.*; 
 
 //The applet code
 public class TestApplet extends Applet {
 
     public void paint(Graphics g) {
 
       //Draw a rectangle width=250, height=100
       g.drawRect(0,0,250,100); 
 
       //Set the color to blue
       g.setColor(Color.blue); 
 
       //Write the message to the web page
       g.drawString("Testing",10,50); 
    }
 } 