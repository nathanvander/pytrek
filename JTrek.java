//Source: https://ifarchive.org/indexes/if-archiveXgamesXsourceXinform.html
//ztrek.inf [29-Feb-2000]
//IFDB entry
//Super Z Trek, a Z-Machine implementation of the classic Star Trek. Written by John Menichelli,
//based on Chris Nystrom C port of a BASIC version.
//!*************************************************************************
//!**
//!**  Super Z Trek: Star Trek for the Z Machine
//!**
//!**  Ported to Inform by John Menichelli
//!**
//!*************************************************************************

//!** The Star Trek game has been around since the dawn of personal computers.
//!** This version, written in Inform by John Menichelli, is just the latest
//!** incarnation of this classic game. If you have any questions, comments
//!** or bug reports, please email them to me at menichel@@0064pixi.com. This
//!** program and its source code are in the public domain.
//!**
//!** This version is based on the C port of an old BASIC program. The C version
//!** was written by Chris Nystrom and is available from:
//!**
//!** http://www.cfi.org/pub/ccn/startrek
//!**
//!** You can contact the author of C port at:
//!**
//!** Chris Nystrom
//!** 1013 Prairie Dove Circle
//!** Austin, Texas  78758
//!**
//!** E-Mail: chris@gnu.ai.mit.edu, nystrom@cactus.org, or ccn@cfi.org
//
//!** The original Super Star Trek game comes from the book "BASIC Computer
//!** Games" edited by David Ahl of Creative Computing fame. It was published
//!** in 1978 by Workman Publishing, 1 West 39 Street, New York, New York,
//!** and the ISBN is: 0-89489-052-3.
//!**
//!** Here is the original BASIC header:
//!**
//!** SUPER STARTREK - MAY 16, 1978 - REQUIRES 24K MEMORY
//!**
//!**        **** STAR TREK ****        ****
//!** SIMULATION OF A MISSION OF THE STARSHIP ENTERPRISE,
//!** AS SEEN ON THE STAR TREK TV SHOW.
//!** ORIGINAL PROGRAM BY MIKE MAYFIELD, MODIFIED VERSION
//!** PUBLISHED IN DEC'S "101 BASIC GAMES", BY DAVE AHL.
//!** MODIFICATIONS TO THE LATTER (PLUS DEBUGGING) BY BOB
//!** LEEDOM - APRIL & DECEMBER 1974,
//!** WITH A LITTLE HELP FROM HIS FRIENDS . . .
//!** COMMENTS, EPITHETS, AND SUGGESTIONS SOLICITED --
//!** SEND TO:  R. C. LEEDOM
//!**           WESTINGHOUSE DEFENSE & ELECTRONICS SYSTEMS CNTR.
//!**           BOX 746, M.S. 338
//!**           BALTIMORE, MD  21203
//!**
//!** CONVERTED TO MICROSOFT 8 K BASIC 3/16/78 BY JOHN BORDERS
//!** LINE NUMBERS FROM VERSION STREK7 OF 1/12/75 PRESERVED AS
//!** MUCH AS POSSIBLE WHILE USING MULTIPLE STATMENTS PER LINE
//!**
//!** Notes on the Inform version:
//!**
//!** Since Inform only works with integers, this version eliminates the
//!** guesswork involved in moving and firing torpedoes. To make up for
//!** this, the torpedo algorithm gives the torped a random chance to miss,
//!** which increases as the range increases.

import java.util.Scanner;

public class JTrek {
	//!** Constants
	public static final int MAX_TORPS = 10;
	public static final int KLINGON_POWER = 200;
	public static final int MAX_POWER= 3000;
	public static final int SCREEN_SIZE =6;
	public static final int ENTERPRISE =1;
	public static final int KLINGON =2;
	public static final int BASE =3;
	public static final int STAR =4;
	public static final int WARP_ENGINES =0;
	public static final int SHORT_RANGE =1;
	public static final int LONG_RANGE =2;
	public static final int PHASER_CONTROL =3;
	public static final int PHOTON_TUBES =4;
	public static final int DAMAGE_CONTROL =5;
	public static final int SHIELD_CONTROL =6;
	public static final int LIBRARY_COMPUTER =7;

	//!** Global Variables
	public static int trek_docked_flag;                //! 1 or 2 if Enterprise is docked
	public static int trek_current_energy;             //! Current energy
	public static int trek_shield_value;               //! Current shield value
	public static int trek_torp_capacity = MAX_TORPS;  //! Photon torpedo capacity
	public static int trek_torps_remaining;            //! Photon torpedoes left
	public static int trek_max_speed;                  //! Maximum allowed speed
	public static int trek_end_of_time;                //! End of time/game
	public static int trek_current_date;               //! Current stardate
	public static int trek_total_bases;                //! Total starbases
	public static int trek_total_klingons;             //! Klingons at start
	public static int trek_klingons_left;              //! Total Klingons left
	public static int trek_quadrant_position;          //! These two variables are used
	public static int trek_sector_position;            //! to calculate the quadrant and
                                        				//! sector location of the Enterprise

    public static Scanner scanner = new Scanner(System.in);

	//!** Arrays
	public static int[] trek_long_range_galaxy = new int[64];	//! Holds long range scan data
	public static int[] trek_galaxy_history = new int[64];      //! Hold history of all long and short range scans
	public static int[] trek_temp_array = new int[64];          //! Used for printing long range scans
	public static int[] trek_sector = new int[64];              // ! Sector data array
	public static int[] trek_damage_array = new int[8];         // ! Damage Array
	public static int[] trek_klingon_array = new int[3];        // ! Array used to track Klingon damage;
	//omit for now - I don't know if these are chars or strings
	//Array text_array -> 60;                 ! Input array for keyboard entry

	//! Main Program
	//[ Main ;
	public static void main(String[] args) {
   		PlayTrek();
	}

	//utility functions
	public static void print(String s) {System.out.println(s);}
	public static void p(String s) {System.out.print(s);}
	public static void p(int i) {System.out.print(i);}

	//return a random number from 0..(i-1)
	public static int random(int i) {
		return (int)(Math.floor(Math.random()*i));
	}

	public static void Pause() {
		System.out.println("(Press Enter to continue)");
		scanner.nextLine();
		//try {
		//	int i = System.in.read();
		//} catch (java.io.IOException ix) {
		//	ix.printStackTrace();
		//	System.out.println("fatal io exception");
		//	System.exit(1);
		//}
	}

	public static void new_line() {
		System.out.println(" ");
	}

	//I am changing this so it just reads the next int
	public static int read_int() {
		return scanner.nextInt();
	}

	public static String next_line() {
		return scanner.nextLine();
	}

	//[ PlayTrek ;
	public static void PlayTrek() {
   		TrekIntro();
   		Initialize();
   		EndScreen();
	}

	//[ TrekIntro ;
	public static void TrekIntro() {
   		//font off;
   		print("************************************");
       	print("*                                  *");
       	print("*                                  *");
       	print("*       * * Super J Trek * *       *");
       	print("*                                  *");
       	print("*                                  *");
       	print("************************************");
   		print("^^^");
   		//spaces (0->33)/2 - 12;
   		Enterprise();

   		Pause();
	}

	//[ Initialize i j bases stars klingons;
	public static void Initialize() {
		int i=0, j=0;
		int bases=0;
		int stars=0;
		int klingons=0;

   		//! Initialize time
   		trek_current_date = (20 + random(10)) * 1000;
   		trek_end_of_time = (25 + random(10)) * 10;

  		//! Setup What Exists in Galaxy
   		for (i = 0; i < 64; i++) {
      		trek_galaxy_history[i] = 999;
		}

   		for (i = 0; i < 64; i++) {
      		j = random(100);
      		if (j>=98) {
				klingons = 3;
			} else if (j>=95) {
				klingons = 2;
			} else if (j>=81) {
				klingons = 1;
			} else {
				klingons = 0;
			}

			trek_klingons_left = trek_klingons_left + klingons;

	 		if (random(100) > 96) {
	    		bases = 1;
	 		} else {
	    		bases = 0;
			}

     		trek_total_bases = trek_total_bases + bases;

      		stars = random(8);

      		trek_long_range_galaxy[i] = (klingons * 100) + (bases * 10) + stars;
   		}

   		if (trek_total_bases == 0) {
      		i = random(64);	// - 1;
      		j = trek_long_range_galaxy[i];
      		j = j + 10;
      		trek_long_range_galaxy[i] = j;
      		trek_total_bases++;
   		}

   		if (trek_klingons_left > trek_end_of_time / 10) {
     		trek_end_of_time = (trek_klingons_left + 1) * 10;
		}

   		trek_total_klingons = trek_klingons_left;

  		//! Initialize Enterprise
   		trek_docked_flag = 0;
   		trek_current_energy = MAX_POWER;
   		trek_torps_remaining = trek_torp_capacity;
   		trek_shield_value = 0;
   		trek_max_speed = 8;
   		trek_quadrant_position = random(64); //- 1;
   		trek_sector_position = random(64); //- 1;

   		for (i = 0; i < 8; i++) {
      		trek_damage_array[i] = 5;
		}

   		MissionBrief();
   		//SetScreen();
   		NewQuadrant();
   		UpdateStatus();
   		ShortRangeScan();
   		MainMenu();
	}

	//[ NewQuadrant i j k b s ;
	public static void NewQuadrant() {
		int i=0, j=0, k=0, b=0, s=0;
   		trek_galaxy_history[trek_quadrant_position] = trek_long_range_galaxy[trek_quadrant_position];

   		for (i = 0; i < 3; i++) {
      		trek_klingon_array[i] = KLINGON_POWER;
		}

   		i = trek_long_range_galaxy[trek_quadrant_position];

   		k = i / 100;                     //! Klingons
   		b = i / 10 - (10 * k);           //! Bases
   		s = i - (100 * k) - (10 * b);    //! Stars

   		for (i = 0; i < 64; i++) {
      		trek_sector[i] = 0;
		}

   		trek_sector[trek_sector_position] = ENTERPRISE;

   		for (i = 1; i <= k; i++)         //! Position Klingons
   		{
			Retry1: {
      			j = random(64);	// - 1;
      			if (trek_sector[j] == 0) {
        		 	break Retry1;
      			} else {
        			trek_sector[j] = KLINGON;
	 			}
			}
   		}

	   	for (i = 1; i <= b; i++)         //! Position base
	   	{
			Retry2: {
				j = random(64);	// - 1;
				if (trek_sector[j] == 0) {
	        	 	break Retry2;
		 		} else {
	        		trek_sector[j] = BASE;
				}
			}
	   	}

   		for (i = 1; i <= s; i++)         //! Position stars
   		{
			Retry3: {
      			j = random(64); //- 1;
      			if (trek_sector[j] == 0) {
      	   			break Retry3;
				} else {
         			trek_sector[j] = STAR;
				}
			}
   		}
	}

//[ SetScreen i j;
//   @erase_window $ffff;
//   @split_window SCREEN_SIZE;
//   @set_window 1;
//   style reverse;
//   j = SCREEN_SIZE;
//   for (i = 1 : i <= j: i++)
//   {
//      @set_cursor i 1;
//      spaces (0->33)-1;
//   }
//   style roman;
//];

	//[ MissionBrief ;
	public static void MissionBrief() {
   		//@erase_window $ffff;
   		new_line();
   		new_line();
   		print("To:      Captain, USS Enterprise, NCC-1701");
		print(" ");
   		print("From:    Starfleet Command");
		print(" ");
   		print("Subject: War Warning");
		print(" ");
   		print("1. Approximately three (3) hours ago, warships of the Imperial");
        print("Klingon Empire Navy crossed the border into Federation space. These");
        print("vessels have destroyed all outposts and ships in their path and");
        print("have not answered any hails.");
		print(" ");
   		print("2. Therefore, effective immediately, a state of war exists between");
        print("the United Federation of Planets and the Imperial Klingon");
        print("Empire.");
		print(" ");
   		print("3. As the Enterprise is the only vessel available in this portion");
        print("of the galaxy, your orders are as follows:");
		print(" ");
   		print("4. Engage and destroy any and all Klingon vessels you encounter");
        print("within your designated patrol zone. Long range sensor scans indicate");
        print("a total of " + trek_klingons_left + " Klingon battlecruisers in your area.");
		print(" ");
   		print("5. Starfleet Operations calculates that it will take");
        print("approximately " + (trek_end_of_time / 10 ) + " days to mobilize our");
        print("forces and begin sending reinforcements to the front. We need you");
        print("to hold off the invading Klingon fleet until those reinforcements");
        print("arrive.");
		print(" ");
   		print("6. Good luck and good hunting.");
		print(" ");
   		//print "[Press any key to accept command]";

   		Pause();
	}

	//[ UpdateStatus i;
	public static void UpdateStatus() {
   		//@set_window 1;

   		//@set_cursor 1 1;
   		//style reverse;
   		//for (i = 1: i <= 2: i++) {
      	//@set_cursor i 1;
      	//spaces (0->33)-1; }

		//row 1
   		//@set_cursor 1 1;
   		String curdat = (trek_current_date / 10)+ "." + (trek_current_date % 10);
   		String remdat = (trek_end_of_time / 10) + "." + (trek_end_of_time % 10);
   		print("Current Date: "+curdat + "    " + "Days Remaining: "+remdat);

		//row 2
   		print("Klingons Remaining: " + trek_klingons_left + "    " +"Bases Remaining: "+trek_total_bases);

		//row 3
		int enerem = trek_current_energy + trek_shield_value;
   		print("Shield Value: "+ trek_shield_value+ "    " +"Total Energy Remaining: "+enerem);

		//moved to main menu
  		//print "1: Nav     2: SRS     3: LRS      4: Phaser  5: Torp^";
   		//print "6: Shield  7: Damage  8: Library  9: Help    0: Quit";

   		//@set_cursor 1 15;
   		//print (trek_current_date / 10), ".", (trek_current_date % 10);

   		//if (trek_end_of_time < 100)
   		//   @set_cursor 1 50;
   		//else
   		//   @set_cursor 1 49;

   		//print trek_end_of_time / 10, ".", trek_end_of_time % 10;

   		//@set_cursor 2 21;
   		//print trek_klingons_left;
   		//@set_cursor 2 52;
   		//print trek_total_bases;

   		//@set_cursor 3 15;
   		//print trek_shield_value;
   		//i = trek_current_energy + trek_shield_value;
   		//@set_cursor 3 49;

   		//switch(i)
   		//{
   		//   0 to 9     : print "   ", i;
   		//   10 to 99   : print "  ", i;
   		//   100 to 999 : print " ", i;
   		//   default    : print i;
   		//}

   		//style roman;

   		//@set_window 0;
	}

	//[ MainMenu i ;
	public static void MainMenu() {

   		while(true)
   		{
   			print("1: Nav     2: SRS     3: LRS      4: Phaser  5: Torp");
   			print("6: Shield  7: Damage  8: Library  9: Help    0: Quit");

			int i = read_int();
      		//@read_char 1 -> i;

      		switch(i) {
         		case 0 : break;
         		case 1 : CourseControl(); break;
         		case 2 : ShortRangeScan(); break;
         		case 3 : LongRangeScan(); break;
         		case 4 : PhaserControl(); break;
         		case 5 : PhotonTorps(); break;
         		case 6 : ShieldControl(); break;
         		case 7 : DamageControl(); break;
         		case 8 : Library(); break;
         		case 9 : Help(); break;
         		default : print("Invalid Command "+i);
      		}
   			if (i == 0) break;
   		}
	}

	//[ CourseControl i course speed;
	public static void CourseControl() {
		print("[CourseControl]");
		int i=0;
		int course=0, speed=0;
   		PrintCompass();

   		print("^Enter course (1-8): ");
   		i = read_int();

   		if (i < 1 || i > 8) {
      		print("^Lt. Sulu reports: ~Incorrect course data, sir!~ ["+i+"]^");
      		return;
		}

   		//course = i - 48;
   		course = i;
   		print("Course: "+course);

   		trek_max_speed = trek_damage_array[WARP_ENGINES];
   		trek_max_speed = trek_max_speed + 3;
   		print("^^Enter warp speed (1-"+ trek_max_speed+ "): ");
   		i = read_int();
   		//speed = i - 48;
   		speed = i;
		print("Attempting warp "+speed);

   		if (speed < 1) {
      		print("^Lt. Sulu reports: ~Incorrect speed, sir!~^^");
      		return;
		}

   		if (speed > trek_max_speed) {
      		print("^Chief Engineer Scott reports: ~The engines won't take more than warp "+ trek_max_speed+ "!~^^");
      		return;
		}

   		if (speed * 10 > trek_current_energy + trek_shield_value) {
      		print("^Chief Engineer Scott reports: ~We don't have enough energy power to go that fast!~^^");
      		return;
  		}

   		trek_current_energy = trek_current_energy - (speed * 10);

   		print("Reaching warp "+ speed + "^^");

  		if (trek_current_energy < 0)
  		{
    		print("^Diverting Shield Control supplies energy to complete the maneuver.^");

    		trek_shield_value = trek_shield_value + trek_current_energy;
     		trek_current_energy = 0;

     		if (trek_shield_value < 0) {
        		trek_shield_value = 0;
			}
   		}
   		CompleteManeuver(course, speed);
   		if (trek_current_energy + trek_shield_value <= 0) {
      		OutOfEnergy();
		}
	}

	//[ CompleteManeuver course speed i j xs ys xq yq;
	public static void CompleteManeuver(int course,int speed) {
		int i=0, j=0, xs=0, ys=0, xq=0, yq=0;
		print("[CompleteManeuver("+course+","+speed+")]");
   		xs = (trek_sector_position % 8) + 1;
   		ys = 8 - (trek_sector_position / 8);

   		xq = (trek_quadrant_position % 8) + 1;
   		yq = 8 - (trek_quadrant_position / 8);

   		j = trek_sector_position;

   		for (i = 1; i <= speed; i++)
   		{

      		if (OutOfBounds(course) == 1)
      		{
            	print("^Movement aborted - you may not leave your designated patrol area.^");
            	break;
      		}

      		switch(course)
      		{
         		case 1: ys++; break;
         		case 2: xs++; ys++; break;
         		case 3: xs++; break;
         		case 4: xs++; ys--; break;
         		case 5: ys--; break;
         		case 6: ys--; xs--; break;
         		case 7: xs--; break;
         		case 8: xs--; ys++; break;
         		default: print("Unable to complete maneuver "+course);
      		}

      		if (xs < 1 || xs > 8 || ys < 1 || ys > 8)
      		{
      		   if (xs < 1) { xs = 8; xq--; }
      		   if (xs > 8) { xs = 1; xq++; }
      		   if (ys < 1) { ys = 8; yq--; }
      		   if (ys > 8) { ys = 1; yq++; }

      		   j = (8 * (8 - ys)) + xs - 1;
      		   trek_sector_position = j;
      		   trek_quadrant_position = (8 * (8 - yq)) + xq - 1;
      		   if (trek_docked_flag > 0) {
      		      trek_docked_flag = 0;
			  }
      		   NewQuadrant();
      		}
		    else
		    {
		         j = (8 * (8 - ys)) + xs - 1;

    		     if (trek_sector[j] == KLINGON || trek_sector[j] == STAR) //! You can pass through a base
    		     {
    		        print ("^Movement aborted due to improper navigation.^");
    		        break;
    		     }
		         if (trek_sector[j] == BASE)
		         {
		            if (i == speed)
		            {
		               print ("^The Enterprise is now docked.^");
		               trek_docked_flag = 1;
		               trek_sector[trek_sector_position] = 0;
		               trek_sector_position = j;
		              // jump DoneMoving;
						DoneMoving(speed);
		            }
		            else {
		               continue;
				   }
		        }
         		else
         		{
         			trek_sector[j] = ENTERPRISE;
         		   	if (trek_docked_flag > 0)
         		   	{
       		       		trek_docked_flag = 0;
       		        	trek_sector[trek_sector_position] = BASE;
       		     	}
            		else
					{
               			trek_sector[trek_sector_position] = 0;
					}
            		trek_sector_position = j;
         		}
      		}
   		}
	}
	//!.DoneMoving;

	public static void DoneMoving(int speed) {
		print("[DoneMoving("+speed+")]");
   		trek_current_date = trek_current_date + speed;
   		trek_end_of_time = trek_end_of_time - speed;
   		if (trek_end_of_time <= 0) {
      		EndOfTime();
		}
   		UpdateStatus();
   		DamageRepair();
   		UpdateStatus();
   		ShortRangeScan();
	}

	//[ OutOfBounds course xs ys xq yq;
	public static int OutOfBounds(int course) {
		//print("[OutOfBounds("+course+")]");
		if (course<1 || course>8) {
			print("Invalid course: "+course);
			return 0;
		}
		int xs = 0, ys = 0, xq = 0, yq = 0;
   		xs = (trek_sector_position % 8) + 1;
   		ys = 8 - (trek_sector_position / 8);

   		xq = (trek_quadrant_position % 8) + 1;
   		yq = 8 - (trek_quadrant_position / 8);

   		if (xq == 1 && yq == 1 && xs == 1 && ys == 1) //! Lower left corner
   		{
   		   //if (course == 4 or 5 or 6 or 7 or 8)
   		   if (course > 3)
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (xq == 8 && yq == 8 && xs == 8 && ys == 8) //! Upper right corner
   		{
   		   //if (course == 1 or 2 or 3 or 4 or 8)
   		   if (course < 5 || course==8)
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (xq == 8 && yq == 1 && xs == 8 && ys == 1) //! Lower right corner
   		{
   		   //if (course == 2 or 3 or 4 or 5 or 6)
   		   if (course > 1 && course < 7 )
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (xq == 1 && yq == 8 && xs == 1 && ys == 8) //! Upper left corner
   		{
   		   //if (course == 1 or 2 or 6 or 7 or 8)
   		   if (course <3 || course > 5)
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (xq == 1 && xs == 1) //! Left edge
   		{
      		//if (course == 6 or 7 or 8)
      		if (course > 5)
         		return 1;
      		else
         		return 0;
   		}

   		if (xq == 8 && xs == 8) //! Right Edge
   		{
   		   //if (course == 2 or 3 or 4)
   		   if (course > 1 && course < 5)
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (yq == 8 && ys == 8) //! Top edge
   		{
   		   //if (course == 1 or 2 or 8)
   		   if (course < 3 || course == 8)
   		      return 1;
   		   else
   		      return 0;
   		}

   		if (yq == 1 && ys == 1) //! Bottom edge
   		{
      		//if (course == 4 or 5 or 6)
      		if (course > 3 && course < 7)
      		   return 1;
      		else
      		   return 0;
   		}

   		return 0;
	}

	//[ PrintCompass ;
	public static void PrintCompass() {
		new_line();
   		print(" 8  1  2");
  		print("  \\ | / ");		//make backslash double
   		print("7  -+-  3");
   		print("  / | \\ ");
   		print(" 6  5  4");
	}

	//[ ShortRangeScan x y ;
	public static void ShortRangeScan() {
		print("[ShortRangeScan]");
		int x=0, y=0;
   		if (trek_damage_array[SHORT_RANGE] < 5) {
      		print ("^Short Range Sensors are inoperative.^");
  		}

   		//! Determine Quadrant

   		x = (trek_quadrant_position % 8) + 1;
   		y = 8 - (trek_quadrant_position / 8);

   		print ("^Short range scan of quadrant ");
   		p(x + ", " + y + " (");
   		//PrintQuadrantName(x, y);
   		p( QuadrantName(x,y) );
   		print(")^^");

   		print ("     1   2   3   4   5   6   7   8^");
   		print ("    --- --- --- --- --- --- --- ---^");
   		for (x = 0; x < 64; x++)
   		{
   		   if (x % 8 == 0)
   		   {
   		      p( " ");
   		      p( (8 - (x/8)) );
   		      p(":");
   		   }

   		   switch (trek_sector[x])
   		   {
   		      case 0 : p( "  . "); break;
   		      case 1 : p(" +E+"); break;
   		      case 2 : p(" +K+"); break;
   		      case 3 : 	if (trek_docked_flag == 0) { p(" >B<");}
						else { p(" >D<");}
						break;
   		      case 4 : p("  # "); break;
   		      default: p(" ");
   		   }

   		   if ((x + 1) % 8 == 0) {
   		      print ("^");
		  }
   		}

   		y = 0;
   		for (x = 1; x < 64; x++) {
   		   if (trek_sector[x] == 2) y++;
		}
   		p("^Alert Condition: ");

   		if (y > 0) {
   		   print ("Red^");
   		} else {
			if (trek_current_energy * 10 < MAX_POWER) {
   		   		print ("Yellow^");
   			} else {
   		   		print ("Green^");
			}
		}

	}	//end ShortRangeScan

	//[ LongRangeScan i j temp_pos;
	public static void LongRangeScan() {
		int i=0, j=0, temp_pos=0;
		print("[LongRangeScan]");
   		if (trek_damage_array[LONG_RANGE] < 5) {
   		   print("^Long Range Sensors are inoperative.^");
		}

   		for (i = 0; i < 64; i++) {
   		   trek_temp_array[i] = 999;
		}

   		temp_pos = trek_quadrant_position;

   		if (temp_pos == 0)   //! Upper left
   		{
   		   trek_temp_array[0] = trek_long_range_galaxy[0];
   		   trek_temp_array[1] = trek_long_range_galaxy[1];
   		   trek_temp_array[8] = trek_long_range_galaxy[8];
   		   trek_temp_array[9] = trek_long_range_galaxy[9];

   		   trek_galaxy_history[0] = trek_long_range_galaxy[0];
   		   trek_galaxy_history[1] = trek_long_range_galaxy[1];
   		   trek_galaxy_history[8] = trek_long_range_galaxy[8];
   		   trek_galaxy_history[9] = trek_long_range_galaxy[9];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

   		if (temp_pos == 7)   //! Upper right
   		{
   		   trek_temp_array[6]  = trek_long_range_galaxy[6];
   		   trek_temp_array[7]  = trek_long_range_galaxy[7];
   		   trek_temp_array[14] = trek_long_range_galaxy[14];
   		   trek_temp_array[15] = trek_long_range_galaxy[15];

   		   trek_galaxy_history[6]  = trek_long_range_galaxy[6];
   		   trek_galaxy_history[7]  = trek_long_range_galaxy[7];
   		   trek_galaxy_history[14] = trek_long_range_galaxy[14];
   		   trek_galaxy_history[15] = trek_long_range_galaxy[15];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

   		if (temp_pos == 56)  //! Lower left
   		{
   		   trek_temp_array[48] = trek_long_range_galaxy[48];
   		   trek_temp_array[49] = trek_long_range_galaxy[49];
   		   trek_temp_array[56] = trek_long_range_galaxy[56];
   		   trek_temp_array[57] = trek_long_range_galaxy[57];

   		   trek_galaxy_history[48] = trek_long_range_galaxy[48];
   		   trek_galaxy_history[49] = trek_long_range_galaxy[49];
   		   trek_galaxy_history[56] = trek_long_range_galaxy[56];
   		   trek_galaxy_history[57] = trek_long_range_galaxy[57];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

   		if (temp_pos == 63)  //! Lower right
   		{
   		   trek_temp_array[54] = trek_long_range_galaxy[54];
   		   trek_temp_array[55] = trek_long_range_galaxy[55];
   		   trek_temp_array[62] = trek_long_range_galaxy[62];
   		   trek_temp_array[63] = trek_long_range_galaxy[63];

   		   trek_galaxy_history[54] = trek_long_range_galaxy[54];
   		   trek_galaxy_history[55] = trek_long_range_galaxy[55];
   		   trek_galaxy_history[62] = trek_long_range_galaxy[62];
   		   trek_galaxy_history[63] = trek_long_range_galaxy[63];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

		if (temp_pos < 8)    //! Top edge
   		{
   		   trek_temp_array[temp_pos]     = trek_long_range_galaxy[temp_pos];
   		   trek_temp_array[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
   		   trek_temp_array[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
   		   trek_temp_array[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
   		   trek_temp_array[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
   		   trek_temp_array[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];

   		   trek_galaxy_history[temp_pos]     = trek_long_range_galaxy[temp_pos];
   		   trek_galaxy_history[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
   		   trek_galaxy_history[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
   		   trek_galaxy_history[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
   		   trek_galaxy_history[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
   		   trek_galaxy_history[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

	   if (temp_pos > 55)   //! Bottom edge
	   {
	      trek_temp_array[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_temp_array[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	      trek_temp_array[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	      trek_temp_array[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	      trek_temp_array[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_temp_array[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];

	      trek_galaxy_history[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_galaxy_history[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	      trek_galaxy_history[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	      trek_galaxy_history[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	      trek_galaxy_history[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_galaxy_history[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
   		}

	   if (temp_pos % 8 == 0)  //! Left edge
	   {
	      trek_temp_array[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_temp_array[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_temp_array[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	      trek_temp_array[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	      trek_temp_array[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	      trek_temp_array[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];

	      trek_galaxy_history[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_galaxy_history[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_galaxy_history[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	      trek_galaxy_history[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	      trek_galaxy_history[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	      trek_galaxy_history[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
	   }
	   if ((temp_pos+1) % 8 == 0)  //! Right edge
	   {
	      trek_temp_array[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_temp_array[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_temp_array[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	      trek_temp_array[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
	      trek_temp_array[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	      trek_temp_array[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];

	      trek_galaxy_history[temp_pos]     = trek_long_range_galaxy[temp_pos];
	      trek_galaxy_history[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	      trek_galaxy_history[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	      trek_galaxy_history[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
	      trek_galaxy_history[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	      trek_galaxy_history[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];

   		   //jump Printit;
   		   PrintLongRangeScanResults();
   		   return;
	   }

   		//! Everything else
	   trek_temp_array[temp_pos]     = trek_long_range_galaxy[temp_pos];
	   trek_temp_array[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];
	   trek_temp_array[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	   trek_temp_array[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	   trek_temp_array[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	   trek_temp_array[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	   trek_temp_array[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
	   trek_temp_array[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	   trek_temp_array[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];

	   trek_galaxy_history[temp_pos]     = trek_long_range_galaxy[temp_pos];
	   trek_galaxy_history[(temp_pos-9)] = trek_long_range_galaxy[(temp_pos-9)];
	   trek_galaxy_history[(temp_pos-8)] = trek_long_range_galaxy[(temp_pos-8)];
	   trek_galaxy_history[(temp_pos-7)] = trek_long_range_galaxy[(temp_pos-7)];
	   trek_galaxy_history[(temp_pos-1)] = trek_long_range_galaxy[(temp_pos-1)];
	   trek_galaxy_history[(temp_pos+1)] = trek_long_range_galaxy[(temp_pos+1)];
	   trek_galaxy_history[(temp_pos+7)] = trek_long_range_galaxy[(temp_pos+7)];
	   trek_galaxy_history[(temp_pos+8)] = trek_long_range_galaxy[(temp_pos+8)];
	   trek_galaxy_history[(temp_pos+9)] = trek_long_range_galaxy[(temp_pos+9)];
   		PrintLongRangeScanResults();

	}	//end LongRangeScan

	//.Printit;
	public static void PrintLongRangeScanResults() {
		print("[PrintLongRangeScanResults]");
		int i=0, j=0;
   		new_line();
   		new_line();

   		print ("                 Long Range Scan Results^^");
   		print ("      1     2     3     4     5     6     7     8^");
   		print ("    ----- ----- ----- ----- ----- ----- ----- -----^");

   		for (i = 0; i < 64; i++)
   		{
   		   if (i%8 == 0)
   		   {
   		      p( " ");
   		      p( 8 - i/8);
   		      p(":");
   	   		}

      		j = trek_temp_array[i];

      		p(" ");

      		//if (i == temp_pos)
      		//   style reverse;
      		//else
      		//   style roman;

      		//switch(j)
      		//{
      		//   0 to 9   : print " 00"; print j;
      		//   10 to 98 : print " 0";  print j;
      		//   999      : print " ***";
      		//   default  : print " "; print j;
      		//}
      		if (j<10) {
				p(" 00"); p(j);
			} else if (j>9 && j<100) {	//what about 99 - is that special
				p(" 0");  p( j);
			} else if (j==999) {
				p(" ***");
			} else {
				p(" "); p(j);
			}

      		p(" ");

      		//style roman;

   			if (i%8 == 7) {
   		   		print( "^");
			}
   		}
	}

	//[ TextToNumber n x len mul tot;
	//This is only called twice, in phaser control and shield control
	//in both cases, it looks like a single digit number will suffice
	//public static int TextToNumber() {
	//	char c = read_char();
	//	return (int)(c-48);
	//}
    //text_array -> 0 = 60;
    //read text_array 0;

    //if (text_array->1 > 4)
    //   return -1;

    //x = 0;
    //len = text_array->1;

    //if (len == 4) mul=1000;
    //if (len == 3) mul=100;
    //if (len == 2) mul=10;
    //if (len == 1) mul=1;

    //tot = 0;

    //for (n = 0: n < len: n++)
    //{
    //   if (text_array->(n+2) > 47 && text_array->(n+2) < 58)
    //   {
    //      x = text_array->(n+2);
    //      x = x - 48;
    //      tot = tot + mul * x;
    //      mul = mul/10;
    //   }
    //   else
    //      return -1;
    //}
    //return tot;
//];	//end TextToNumber

	//[ PhaserControl i j k x1 y1 x2 y2 z rng dmg;
	public static void PhaserControl() {
		int i=0, j=0, k=0, x1=0, y1=0, x2=0, y2=0, z=0, rng=0, dmg=0;
		print("[PhaserControl]");

   		if (trek_damage_array[PHASER_CONTROL] < 5) {
      		print("^Science Officer Spock reports: ~Phasers are inoperative, Captain.~^");
      		return;
  		}

   		k = trek_long_range_galaxy[trek_quadrant_position];

   		k = k / 100;                    // ! Klingons

   		if (k == 0) {
      		print("^Science Officer Spock reports: ~Sensors show no enemy ships in this quadrant~^");
      		return;
		}

   		if (trek_damage_array[LIBRARY_COMPUTER] < 5) {
   	   		print ("^Science Officer Spock reports: ~Computer failure will hamper accuracy, Captain.~^");
   	   		return;
		}

   		print ("^Phasers locked on target. Energy available = " + (trek_current_energy + trek_shield_value) );

   		print ("^Enter number of units to fire: ");

   		//i = TextToNumber();
		i = read_int();

   		if (i <= 0) {
      		print ("^Science Officer Spock reports: ~Phaser fire aborted.~^");
      		return;
		}

   		if (i > trek_current_energy) {
      		print("^Science Officer Spock reports: ~Insufficient energy for that attack.~^");
      		return;
		}

   		trek_current_energy = trek_current_energy - i;

   		if (trek_damage_array[LIBRARY_COMPUTER] < 5) { //! Computer damage affects targeting
      		i = i * trek_damage_array[LIBRARY_COMPUTER] / 5;
		}

   		i = i / k; //! Divide the energy between each target

   		x1 = (trek_sector_position % 8) + 1;
   		y1 = 8 - (trek_sector_position / 8);

   		k = -1;

   		for (j = 0; j < 64; j++)
   		{
      		if (trek_sector[j] == KLINGON)
      		{
         		k++;
         		x2 = (j % 8) + 1;
         		y2 = 8 - (j / 8);

         		rng = Range(x1, y1, x2, y2);

         		dmg = i;

         		dmg = dmg * 10 / (rng + random(5));	// - 1);

         		z = trek_klingon_array[k];

         		if (dmg <= 0) {
            		print("^Science Officer Spock reports: ~Sensors show no damage to");
             		print("the Klingon battlecruiser at " + x2 + ", " + y2 + ".~^");
				}

         		if (dmg >= z)
         		{
            		print("^Science Officer Spock reports: ~The Klingon battlecruiser");
            	    print("at " + x2 + ", " + y2 + " has been destroyed.~^");
            		trek_klingon_array[k] = 0;
            		trek_sector[j] = 0;
            		trek_klingons_left--;
            		if (trek_klingons_left == 0) {
               			WonGame();
					}

            		z = trek_long_range_galaxy[trek_quadrant_position];
            		z = z - 100;
            		trek_long_range_galaxy[trek_quadrant_position] = z;
            		if (z / 100 == 0) {
               			ShortRangeScan();
					}
            		UpdateStatus();
				}
         		else
         		{
            		z = z - dmg;
            		trek_klingon_array[k] = z;
            		print("^Science Officer Spock reports: ~Sensors show that the Klingon");
            		print("battlecruiser at " + x2 + ", " + y2 + " suffered a " + dmg + " unit hit.~^");
         		} //end else
      		}	//end if trek_sector
  	 	} //end for
   		KlingonsShoot();
	}	//end phaser control

	//[ PhotonTorps course i x1 y1 x2 y2 z index ;
	public static void PhotonTorps() {
		int course=0, i=0, x1=0, y1=0, x2=0, y2=0, z=0, index=0;
		print("[PhotonTorps]");
		int i2=0;

   		if (trek_torps_remaining == 0) {
      		print("^Ensign Chekov reports: ~All photon torpedoes expended, sir!~^");
      		return;
		}

   		if (trek_damage_array[PHOTON_TUBES] < 5) {
   		   print("^Ensign Chekov reports: ~Photon torpedo tubes not operational, sir!~^");
   		   return;
		}

   		i = trek_long_range_galaxy[trek_quadrant_position];

   		i = i / 100;                    // ! Klingons

   		if (i == 0) {
      		print("^Ensign Chekov reports: ~There are no Klingons in this quadrant, sir!~^");
      		return;
		}

   		trek_torps_remaining--;
   		x1 = (trek_sector_position % 8) + 1;
   		y1 = 8 - (trek_sector_position / 8);

   		PrintCompass();

   		print ("^Enter torpedo course (1-8): ");

   		i2 = read_int();	// 1 -> i;

   		if (i2 < 1 || i2 > 8) {
   	   		print("^Ensign Chekov reports: ~Incorrect course data ["+i2+"], sir!~^");
   	   		return;
		}

   		//course = c - 48;
		course = i2;

   		print (course + "^");

   		for (i = 1; i < 8; i++)
   		{
      		switch(course)
      		{
		         case 1: y1++; break;
		         case 2: x1++; y1++; break;
		         case 3: x1++; break;
		         case 4: x1++; y1--; break;
		         case 5: y1--; break;
		         case 6: y1--; x1--; break;
		         case 7: x1--; break;
		         case 8: x1--; y1++; break;
		         default: print("Incorrect course "+course);
			}

	      	if (x1 < 1 || x1 > 8 || y1 < 1 || y1 > 8)
      		{
         		print ("^Ensign Chekov reports: ~The torpedo missed, sir!~^");
         		break;
      		}

      		index = (8 * (8 - y1)) + x1 - 1;

      		if (trek_sector[index] == KLINGON)
     		{
         		x2 = (trek_sector_position % 8) + 1;
         		y2 = 8 - (trek_sector_position / 8);

         		z = Range(x1, y1, x2, y2);

         		z = z / 15;

         		//if (random(10) - 1 < z)
         		if (random(10) < z)
         		{
         			print ("^Ensign Chekov reports: ~The torpedo missed, sir!~^");
            		break;
         		}
         		else
         		{
            		trek_sector[index] = 0;
            		trek_klingons_left--;
            		if (trek_klingons_left == 0) {
               			WonGame();
					}
            		z = trek_long_range_galaxy[trek_quadrant_position];
            		z = z - 100;
            		trek_long_range_galaxy[trek_quadrant_position] = z;
            		print ("^Ensign Chekov reports: ~The Klingon battlecruiser in ");
            		print ("sector " + x2 + ", " + y2 + " has been destroyed, sir!~^");
            		UpdateStatus();
            		ShortRangeScan();
            		break;
         		}
      		}

      		if (trek_sector[index] == BASE)
      		{
         		print ("^Ensign Chekov reports: ~You destroyed a base, sir!~^");
         		trek_total_bases--;
         		z = trek_long_range_galaxy[trek_quadrant_position];
         		z = z - 10;
         		trek_long_range_galaxy[trek_quadrant_position] = z;

         		if (trek_total_bases == 0 &&
         		    trek_klingons_left <= (trek_current_date / 10) -
                                   trek_end_of_time / 10)
         		{
            		print ("That does it, Captain!! You are hereby relieved of command");
            	    print ("and sentenced to 99 stardates of hard labor on Cygnus 12!! ");
            		LoseGame();
         		}

         		if (trek_docked_flag > 0) //! Undock
         		{
         		   trek_docked_flag = 0;
         		   trek_sector[trek_sector_position] = ENTERPRISE;
         		   ShortRangeScan();
         		}

         		break;
      		}

      		if (trek_sector[index] == STAR)
      		{
      		   print ("^Ensign Chekov reports: ~The star absorbed the torpedo's energy, sir!~^");
      		   break;
      		}
   		}
   		KlingonsShoot();
	}	//end PhotonTorps

	//[ DamageControl ;
	public static void DamageControl() {
		print("[DamageControl]");
   		new_line();
   		new_line();
   		print ("System                    Status^");
   		print ("-------------------------------------^");

   		p ("Warp Engines              ");
   		if (trek_damage_array[WARP_ENGINES] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Short Range Sensors       ");
   		if (trek_damage_array[SHORT_RANGE] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Long Range Sensors        ");
   		if (trek_damage_array[LONG_RANGE] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Phaser Control            ");
   		if (trek_damage_array[PHASER_CONTROL] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Photon Torpedo Tubes      ");
   		if (trek_damage_array[PHOTON_TUBES] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Damage Control            ");
   		if (trek_damage_array[DAMAGE_CONTROL] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Shield Control            ");
   		if (trek_damage_array[SHIELD_CONTROL] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

   		p ("Library-Computer          ");
   		if (trek_damage_array[LIBRARY_COMPUTER] == 5)
      		print ("Operational^");
   		else
      		print ("Damaged^");

      	new_line();
	} //end DamageControl


	//[ ShieldControl i;
	public static void ShieldControl() {
		int i=0;
		print("[ShieldControl]");
   		if (trek_damage_array[SHIELD_CONTROL] < 5) {
      		print("Shield Control is inoperative.");
		}

   		print ("^Total energy available = " + ( trek_current_energy + trek_shield_value) );

   		print ("^Input number of units to shields: ");

   		//i = TextToNumber();
		i = read_int();

   		if (i == -1) {
      		print ("^Shield Control reports: ~Invalid request - shields unchanged.~^");
      		return;
		}

   		if (i == trek_shield_value) {
      		print("^<Shields Unchanged>^");
      		return;
		}

   		if (i >= trek_current_energy + trek_shield_value) {
       		print("^Shield Control reports: ~There is insufficient energy available - shields unchanged.~^");
       		return;
		}

   		trek_current_energy = trek_current_energy + trek_shield_value - i;
   		trek_shield_value = i;

   		print ("^Shield Control reports: ~Shields now at " + trek_shield_value + " units per your command.~^");
   		UpdateStatus();
	}	//end ShieldControl


	//[ Library i;
	public static void Library() {
		int i = 0;
		print("[Library]");
   		if (trek_damage_array[LIBRARY_COMPUTER] < 5) {
      		print("^The Library Computer is inoperative.^");
		}

   		print ("^Choose which library-computer function you wish to use:^^");
   		print ("1: Galactic Record^");
   		print ("2: Status Report^");
   		print ("3: Exit^^");
   		print ("Enter choice: ");

   		i = read_int();	//@read_char 1 -> i;

   		//System.out.println("(choice='"+i+"')");
   		switch(i)
   		{
   		   case 1 : GalacticRecord(); break;
   		   case 2 : StatusReport(); break;
   		   case 3 : print("^Library-computer exited.^^"); break;
   		   default: print("^Invalid choice.^ '"+i+"'");
   		}
	} //end Library


	//[ GalacticRecord i j;
	//can this be combined with PrintLongRangeScanResults
	public static void GalacticRecord() {
		int i=0,j=0;
		print("[GalacticRecord]");
   		new_line();
   		new_line();

   		print ("                        The Galaxy^^");
   		print ("      1     2     3     4     5     6     7     8^");
   		print ("    ----- ----- ----- ----- ----- ----- ----- -----^");

   		for (i = 0; i < 64; i++)
   		{
      		if (i%8 == 0)
      		{
         		p(" ");
         		p(8 - i/8);
         		p(":");
      		}

      		j = trek_galaxy_history[i];

      		//if (i == trek_quadrant_position)
         	//	style reverse;
      		//else
         	//	style roman;
         	if (i == trek_quadrant_position) { p("!");}
         	else {p (" ");}

      		//switch(j)
      		//{
         	//	0 to 9   : print " 00"; print j;
         	//	10 to 98 : print " 0";  print j;
         	//	999      : print " ***";
         	//	default  : print " "; print j;
      		//}

      		if (j<10) {
				p(" 00"); p(j);
			} else if (j>9 && j<100) {	//what about 99 - is that special
				p(" 0");  p( j);
			} else if (j==999) {
				p(" ***");
			} else {
				p(" "); p(j);
			}
			if (i == trek_quadrant_position) { p("!");}
			else { p (" ");}

      		//style roman;

   			if (i%8 == 7) {
      			print ("^");
			}
   		}
	}	//end Galactic Record

	//[ StatusReport i j x y;
	public static void StatusReport() {
		int i=0, j=0, x=0, y=0;
		print("[StatusReport]");
   		for (i = 1; i < 64; i++) {
      		if (trek_sector[i] == KLINGON) j++;
		}

   		print ("^Status Report:^^");

   		print ("Stardate: " + (trek_current_date / 10) + "." +
          		(trek_current_date % 10) + "^^");

  		print ("Time remaining in mission: " + trek_end_of_time / 10 + "." +
          		(trek_end_of_time % 10) + " days^^");

   		x = (trek_quadrant_position % 8) + 1;
   		y = 8 - (trek_quadrant_position / 8);

   		print ("Position:^^");
   		p ("   Quadrant: " + x + ", " + y + " (");
   		//PrintQuadrantName(x, y);
   		p( QuadrantName(x,y));
   		print (")^^");

   		x = (trek_sector_position % 8) + 1;
   		y = 8 - (trek_sector_position / 8);

   		print ("   Sector:   " +  x + ", " + y + "^^");

   		p ("Alert Condition: ");

   		if (j > 0)
      		print ("Red^^");
   		else if (trek_current_energy * 10 < MAX_POWER)
     		 print ("Yellow^^");
   		else
     		 print ("Green^^");

   		print ("Klingon warships remaining: " + trek_klingons_left + "^^");

   		print ("Total bases remaining: " + trek_total_bases + "^^");

   		print ("Total energy remaining: " + trek_current_energy +
        	trek_shield_value + "^^");

   		print ("Current shield setting: " + trek_shield_value + "^^");

   		print ("Total torpedoes remaining: " + trek_torps_remaining + "^");
	}	//end StatusReport

	//[ KlingonsShoot i j k x1 y1 x2 y2 rng dmg;
	public static void KlingonsShoot() {
		int i=0, j=0, k=0, x1=0, y1=0, x2=0, y2=0, rng=0, dmg=0;

   		i = trek_long_range_galaxy[trek_quadrant_position];

  		i = i / 100;                     //! Klingons

   		if (i == 0) return;

   		if (trek_docked_flag > 0) {
      		print("^Starbase shields protect the Enterprise^^");
      		return;
		}

   		j = -1;
   		for (k = 0; k < 64; k++)
   		{
      		if (trek_sector[k] == KLINGON)
      		{
         		j++;
         		x1 = (k % 8) + 1;
         		y1 = 8 - (k / 8);

         		x2 = (trek_sector_position % 8) + 1;
         		y2 = 8 - (trek_sector_position / 8);

         		rng = Range(x1, y1, x2, y2);

         		dmg = trek_klingon_array[j];

         		x2 = trek_klingon_array[j];

         		x2 = x2 * 2 / 3; //! Reduce available Klingon energy by 1/3

         		trek_klingon_array[j] = x2;

         		dmg = dmg * 10 / (rng + random(5) );	// - 1);

         		print ("^The Klingon battlecruiser at " + x1 + ", " + y1 +
               		" fires on you for " + dmg + " units of damage.^");

         		if (dmg > trek_shield_value)
         		{
            		ShipDestroyed();
         		}
         		else
         		{
            		trek_shield_value = trek_shield_value - dmg;
            		print ("^Shield energy is down to " + trek_shield_value + " units.^");
            		if (dmg >= 20)
            		{
               			if (random(10) < 7 || (dmg * 10 / trek_shield_value > 2))
               			{
                  			dmg = random(8);	// - 1;
                  			if (trek_damage_array[dmg] > 0)
                  			{
                     			x2 = trek_damage_array[dmg];
                     			x2--;
                     			trek_damage_array[dmg] = x2;
                 			}
                  			print ("^Damage control reports: ~");
                  			switch(dmg)
                  			{
                     			case 0 :  p("The warp engines were"); break;
                     			case 1 :  p("The short range sensors were"); break;
                     			case 2 :  p("The long range sensors were"); break;
                    			case 3 :  p("Phaser controls were"); break;
                     			case 4 :  p("The photon torpedo tubes were"); break;
                     			case 5 :  p("Damage control was"); break;
                     			case 6 :  p("Shield control was"); break;
                     			case 7 :  p("The library-computer was"); break;
                     			default:
                  			}
                  			print (" damaged in the attack.~^");
               			}
           			 } //if dmg
         		}	//else
      		}
   		}	//for
   		KlingonsMove();
   		UpdateStatus();
   		ShortRangeScan();
	}	//end KlingonsShoot

	//[ KlingonsMove i j k;
	public static void KlingonsMove() {
   		int i=0,j = 0,k=0;

   		for (i = 0; i < 64; i++)
   		{
      		if (trek_sector[i] == KLINGON)
      		{
         		j++;                  //! Count the number of Klingons in the sector
         		trek_sector[i] = 0;   //! and zero their location
      		}
   		}

   		for (i = 1; i <= j; i++)   //! Position Klingons
   		{
			Retry4: {
      			k = random(64);	// - 1;
      			if (trek_sector[k] == 0) {
         			break Retry4;
	 			}
			}
      		//else
      		//{
         		trek_sector[k] = KLINGON;
			//}
   		}

   		if (trek_klingon_array[0] == 0) {    //! "Garbage collect" the damage array
      		trek_klingon_array[0] = trek_klingon_array[1];
		}

   		if (trek_klingon_array[1] == 0) {
      		trek_klingon_array[1] = trek_klingon_array[2];
		}
	}	//end KlingonsMove

	//[ DamageRepair i j k;
	public static void DamageRepair() {
		int i=0, j=0, k=0;

   		if (trek_docked_flag == 1) //! Docked
   		{
      		trek_docked_flag = 2;
      		trek_current_energy = MAX_POWER;
      		trek_torps_remaining = trek_torp_capacity;
      		if (trek_shield_value > 0) {
         		print ("^Shields dropped for docking purposes.^");
			}

      		trek_shield_value = 0;

      		j = 0;
      		for (i = 0; i < 8; i++)
      		{
         		if (trek_damage_array[i] < 5) {
         			j = j + (5 - trek_damage_array[i]);
				}
      		}

      		if (j > 0)
      		{
         		print ("^Technicians are standing by to effect repairs to your ship.");
         	    print ("These repairs will take " + (j / 10) + "." + (j % 10) + " days to ");
         	    print ("complete. Will you authorize the repair order? (Y/N) ");

         		//c = read_char();	//->k;
         		String s = next_line();
         		//if (c == 'Y' || c == 'y')
         		if (s.equalsIgnoreCase("Y"))
         		{
            		trek_current_date = trek_current_date + j;
            		trek_end_of_time = trek_end_of_time - j;
            		if (trek_end_of_time <= 0) {
               			EndOfTime();
					}
            		for (i = 0; i < 8; i++) {
               			trek_damage_array[i] = 5;
					}
            		print ("^");
         		}
         		else
         		{
            		print (s+"^");
				}
      		}
   		}	//if trek_docked_flag
   		else
   		{
      		k = trek_damage_array[DAMAGE_CONTROL];
      		for (i = 0; i < 8; i++)
      		{
         		if (trek_damage_array[i] < 5 && random(20) < k)
         		{
            		j = trek_damage_array[i];
            		j++;
            		trek_damage_array[i] = j;
            		print ("^Damage control reports: ~The ");

            		switch(i)
            		{
               			case 0 : p("warp engines have"); break;
               			case 1 : p("short range sensors have"); break;
               			case 2 : p("long range sensors have"); break;
               			case 3 : p("phaser control system has"); break;
               			case 4 : p("photon torpedo tubes have"); break;
               			case 5 : p("damage control system has"); break;
               			case 6 : p("shield control system has"); break;
               			case 7 : p("library-computer has"); break;
               			default:
            		}
            		if (j < 5)
               			print (" been partially repaired.~^");
            		else {
               			print (" been completely repaired.~^");
					}
         		} //if trek_damage
      		} //for
   		} //else
	}	//end DamageRepair


	//[ PrintQuadrantName x y;
	public static String QuadrantName(int x,int y) {
		String galaxy = null;
		String quadrant = null;
   		if (x == 1 || x == 2)
   		{
   		   if (y == 1 || y == 2)
   		      galaxy = "Antares";
   		   if (y == 3 || y ==4)
   		      galaxy = "Rigel";
   		   if (y == 5 || y ==6)
   		      galaxy = "Procyon";
   		   if (y == 7 || y ==8)
   		      galaxy = "Vega";
   		}
   		if (x == 3 || x== 4)
   		{
   		   if (y == 1 || y ==2)
   		      galaxy = "Canopus";
   		   if (y == 3 || y ==4)
   		      galaxy = "Altair";
   		   if (y == 5 || y ==6)
   		      galaxy = "Sagittarius";
   		   if (y == 7 || y ==8)
   		      galaxy = "Pollux";
   		}
   		if (x == 5 || x==6)
   		{
   		   if (y == 1 || y ==2)
   		      galaxy = "Sirius";
   		   if (y == 3 || y ==4)
   		      galaxy = "Deneb";
   		   if (y == 5 || y ==6)
   		      galaxy = "Capella";
   		   if (y == 7 || y ==8)
   		      galaxy = "Betelgeuse";
   		}
   		if (x == 7 || x==8)
   		{
   		   if (y == 1 || y ==2)
   		      galaxy = "Aldebaran";
   		   if (y == 3 || y ==4)
   		      galaxy = "Regulus";
   		   if (y == 5 || y ==6)
   		      galaxy = "Arcturus";
   		   if (y == 7 || y ==8)
   		      galaxy = "Spica";
   		}

   		//if (x == 1 or 3 or 5 or 7)
   		if ( (x % 2) == 1)
   		{
   		   //if (y == 1 or 3 or 5 or 7)
   		   if ( (y % 2) == 1)
   		      quadrant = " I";
   		   else
   		      quadrant = " III";
   		}

   		//if (x == 2 or 4 or 6 or 8)
   		if ( (x % 2) == 0)
   		{
   		   //if (y == 1 or 3 or 5 or 7)
   		   if ( (y % 2) == 1)
   		      quadrant = " II";
   		   else
   		      quadrant = " IV";
   		}
   		return galaxy + quadrant;
	}

	//[ Range x1 y1 x2 y2 delta_x delta_y result;
	public static int Range(int x1, int y1,int x2,int y2) {
		int delta_x=0, delta_y=0, result=0;
   		delta_x = (x1 - x2) * 10;
   		delta_x = delta_x * delta_x;

   		delta_y = (y1 - y2) * 10;
   		delta_y = delta_y * delta_y;

   		result = SquareRoot(delta_x + delta_y);

  		return result;
	}


	//! Brute force approach to finding the square root of a number
	//[ SquareRoot a b;
	public static int SquareRoot(int a) {
   		//for (b = 1: b <= 110: b++)
   		//{
      	//if (b * b > a)
        // return (b - 1);
   		//}
   		return (int)Math.sqrt(a);
	}

	//[ ShipDestroyed ;
	public static void ShipDestroyed() {
   		print("The Enterprise has been destroyed. You have failed. ");
   		LoseGame();
	}

	//[ OutOfEnergy ;
	public static void OutOfEnergy() {
   		print("^You've stranded yourself in space without enough energy to get to a base! ");
   		LoseGame();
	}

	//[ EndOfTime ;
	public static void EndOfTime() {
   		print ("You've run out of time, Captain! ");
   		LoseGame();
	}

	//[ LoseGame ;
	public static void LoseGame() {
   		print ("It is stardate " + (trek_current_date / 10) + "." +(trek_current_date % 10) + ". ");

   		//print "There ";
		p("There ");

   		if (trek_klingons_left == 1) {
   		   //print "was ";
   		   p("was ");
	    }
   		else
   		{
   		   //print "were ";
   		   p("were ");
		}
   		p( trek_klingons_left+ " Klingon battlecruiser");

   		if (trek_klingons_left == 1)
   		   p("s");

   		print (" left at the end of your mission.^^");

   		//print "[Press any key to continue.]^";
   		Pause();
   		EndScreen();
	}

	//[ WonGame ;
	public static void WonGame() {
   		print ("Congratulations, Captain! You have destroyed the last Klingon battlecruiser in your patrol area.^^");
		print ("Starfleet awards you the Medal of Valor");
   		//print "[Press any key to continue.]^";
   		Pause();
   		EndScreen();
	}

	//[ EndScreen ;
	public static void EndScreen() {
   		//@set_cursor 1 1;
   		//@split_window 0;
   		//@erase_window $ffff;

   		print ("^Thanks for playing Super Z Trek.^^");
   		//@quit;
   		System.exit(0);
	}

	//[ Pause dummy;
	//@read_char 1 dummy;
	//return dummy;
	//];

	//[ Help i;
	public static void Help() {
		print("[Help]");
   		print("^Choose which file to read:^^");
   		print("1: How To Play Super Z Trek^");
   		print("2: About This Game^");
   		print("3: Exit^^");
   		print("Enter choice: ");

		int i = read_int();
   		//@read_char 1 -> i;
   		//print i - 48, "^";
   		switch(i)
   		{
   		   case 1 : HowToPlay(); break;
   		   case 2 : About(); break;
   		   case 3 : print("^Library-computer exited.^^"); break;
   		   default: print("^Invalid choice.^ '"+(int)i+"'");
   		}
	}

	//[ HowToPlay ;
	public static void HowToPlay() {
   		print ("^Welcome to Super Z Trek, the classic computer game ported to the");
   		print ("Z machine.^^");
		new_line();
   		print ("The Z Trek galaxy is divided into an 8 x 8 quadrant grid, and each");
   		print ("quadrant is further divided into an 8 x 8 sector grid.^^");
		new_line();
   		print ("You will be assigned a starting point somewhere in the galaxy to");
   		print ("begin a tour of duty as captain of the starship Enterprise. Your");
   		print ("mission: to seek out and destroy a fleet of Klingon warships which");
   		print ("have invaded the United Federation of Planets.^^");

   		print ("COMMANDS^^");
		new_line();
   		print ("The menu bar at the top of the screen displays information about the");
   		print ("current game and a list of allowable commands. Each command (numbered");
   		print ("'1' through '0') is activated by pressing the appropriate key. Each");
   		print ("key only has to be pressed once; you do not have to press 'Enter'");
   		print ("to complete the command. Each command is described below.^^");
		new_line();
   		print ("1. Nav: This command is used to move the Enterprise around the");
   		print ("galaxy. Two additional pieces of information are required to");
   		print ("complete this command: course and speed. Course is an integer");
   		print ("from 1 to 8, as follows:^^");
		new_line();
   		PrintCompass();
		new_line();
   		print ("^As with the command keys, only one keypress is required to enter");
   		print ("the course.^^");
		new_line();
		Pause();
   		print ("The second entry is the speed, which is also an integer. The");
   		print ("Enterprise's speed ranges from 1 up to a maximum of 8, but this");
   		print ("maximum may be reduced due to damage to the warp engines. Speed is");
   		print ("entered in the same way as course, with only one keypress");
   		print ("required.^^");
		new_line();
   		print ("If you wish to abort the movement command, enter an invalid value");
   		print ("for either the course or speed.^^");
   		Pause();
		new_line();
   		print ("2. SRS: This command prints out the results of a Short Range Sensor");
   		print ("scan. The print out shows what occupies the Enterprise's current");
   		print ("quadrant. The symbols used are:^^");
		new_line();
   		print ("     +E+ = Your starship's position^");
   		print ("     +K+ = Klingon battlecruiser^");
   		print ("     >B< = Federation starbase (Refuel/Repair/Re-Arm here)^");
   		print ("     >D< = Federation starbase with the Enterprise docked^");
   		print ("      #  = Star^");
   		print ("      .  = Empty space^^");
		new_line();
   		print ("3. LRS: This shows shows conditions in space for one quadrant on");
   		print ("each side of the Enterprise (which is in the middle of the scan");
   		print ("in reverse video). The scan is coded in the form ~###~ where the");
   		print ("units digit is the number of stars, the tens digit is the number");
   		print ("of starbases, and the hundreds digit is the number of Klingons.^^");
		new_line();
   		print ("Example: 207 = 2 Klingons, No Starbases, and 7 stars.^^");
		new_line();
		Pause();
   		print ("4. Phaser: Allows you to destroy the Klingon battlecruisers by");
   		print ("zapping them with suitably large units of energy to deplete their");
   		print ("shield power. With this command, you must enter the number of units");
   		print ("of energy you want to fire, then press the 'Enter' key. The amount");
   		print ("of energy you use will be divided evenly between all of the Klingons");
   		print ("in the quadrant.^^");
		new_line();
   		print ("5. Torp: This commands fires one photon torpedo at one Klingon");
   		print ("ship. You will have to enter the torpedo's course, which is the");
   		print ("same used in movement. If you hit the Klingon vessel, it is");
   		print ("destroyed and cannot fire back at you. If you miss, you are subject");
   		print ("to the disrupter fire of all other Klingons in the quadrant.^^");
		new_line();
   		print ("Note: Since Inform only works with integers, this version");
   		print ("eliminates the guesswork involved in moving and firing torpedoes.");
   		print ("To make up for this, the torpedo algorithm gives the torpedo a");
   		print ("random chance to miss, which increases as the range increases.^^");
		new_line();
   		print ("6. Shield: This command defines the number of energy units to be");
   		print ("assigned to the shields. Energy for the shields is taken from the");
   		print ("ship's total energy.");
   		print ("If the Enterprise is hit and the shield value is reduced to zero or");
   		print ("less, the Enterprise is destroyed. Don't forget to put energy into");
   		print ("the shields before entering combat! Note that the ~Total Energy");
   		print ("Remaining~ heading on the menu bar includes shield energy.^^");
		new_line();
   		print ("7. Damage: This command shows the state of repair of all devices,");
   		print ("either ~Operational~ or ~Damaged.~ If a device is damaged, the");
   		print ("ship's crew will attempt to repair it each time the ship moves.");
   		print ("All damaged may be repaired while docked at a starbase. To dock,");
   		print ("simply move into the same sector as the starbase.^^");
		new_line();
   		print ("8. Library: The library-computer has two functions: ^^");
		new_line();
   		print ("Function 1: Cumulative Galactic Record. This shows computer");
   		print ("memory of the results of all previous short and long range sensor");
   		print ("scans.^^");
		new_line();
   		print ("Function 2: Status Report. This function shows the number of");
   		print ("Klingons, stardates, and starbases remaining in the game.^^");
		new_line();
   		print ("9. Help: Brings up the help menu.^^");
		new_line();
   		print ("0. Quit: Quits the game.^^");
   		new_line();

	}

//[ About ;
	public static void About() {
		print("This is a Java version of the Star Trek game based on an");
		print("Inform version dated 2/28/2000 found at:");
		print("https://ifarchive.org/if-archive/games/source/inform/ztrek.inf");
		print("The previous history is as follows:");
		print(" ");
   		print("^The Star Trek game has been around since the dawn of personal");
        print("computers. This version, written in Inform by John Menichelli,");
        print("is just the latest incarnation of this classic game. If you");
        print("have any questions, comments or bug reports, please email them to");
        print("me at menichel@@0064pixi.com. This program and its source code are");
        print("in the public domain.^^");
		print(" ");
   		print("The Inform version is based on the C port of an old BASIC program.");
        print("The C version was written by Chris Nystrom and is available");
        print("from:^^");
		print(" ");
   		print("http://www.cfi.org/pub/ccn/startrek^^");
		print(" ");
   		print("You can contact the author of the C port at:^^");
		print(" ");
   		print ("Chris Nystrom^");
        print("1013 Prairie Dove Circle^");
        print("Austin, Texas  78758^^");
        print("E-Mail: chris@@0064gnu.ai.mit.edu, nystrom@@0064cactus.org,");
        print("or ccn@@0064cfi.org^^");
		print(" ");
   		print("The original Super Star Trek game comes from the book ~BASIC");
        print("Computer Games~ edited by David Ahl of Creative Computing fame. It");
        print("was published in 1978 by Workman Publishing, 1 West 39 Street,");
        print("New York, New York, and the ISBN is: 0-89489-052-3.^^");
		print(" ");
   		print("Here is the original BASIC header:^^");
		print(" ");
   		print ("SUPER STARTREK - MAY 16, 1978 - REQUIRES 24K MEMORY^^");
		print(" ");
   		print("      **** STAR TREK ****^");
		print(" ");
   		print("SIMULATION OF A MISSION OF THE STARSHIP ENTERPRISE,^");
   		print("AS SEEN ON THE STAR TREK TV SHOW.^");
   		print("ORIGINAL PROGRAM BY MIKE MAYFIELD, MODIFIED VERSION^");
   		print("PUBLISHED IN DEC'S ~101 BASIC GAMES~, BY DAVE AHL.^");
   		print("MODIFICATIONS TO THE LATTER (PLUS DEBUGGING) BY BOB^");
   		print("LEEDOM - APRIL & DECEMBER 1974,^");
   		print("WITH A LITTLE HELP FROM HIS FRIENDS . . .^");
   		print("COMMENTS, EPITHETS, AND SUGGESTIONS SOLICITED --^");
   		print("SEND TO:  R. C. LEEDOM^");
   		print("          WESTINGHOUSE DEFENSE & ELECTRONICS SYSTEMS CNTR.^");
   		print("          BOX 746, M.S. 338^");
   		print("          BALTIMORE, MD  21203^^");
		print(" ");
   		print("CONVERTED TO MICROSOFT 8 K BASIC 3/16/78 BY JOHN BORDERS^");
   		print("LINE NUMBERS FROM VERSION STREK7 OF 1/12/75 PRESERVED AS^");
   		print("MUCH AS POSSIBLE WHILE USING MULTIPLE STATMENTS PER LINE^^");
   		new_line();
	}

	public static void Enterprise() {
		//from https://www.asciiart.eu/television/star-trek
print("     ___________________________            ____");
print("...  \\____NCC_1701A_________|_// __=*=__.--'----'--._________");
print("                    \\  |        /-------.__________.--------'");
print("               /=====\\ |======/      '     '----'");
print("                  \\________          }]");
print("                           `--------'		");
	}

	public static void Enterprise2() {
print("___________________          _-_");
print("\\==============_=_/ ____.---'---`---.____");
print("            \\_ \\    \\----._________.----/");
print("              \\ \\   /  /    `-_-'");
print("          __,--`.`-'..'-_");
print("         /____          ||");
print("              `--.____,-'	");
	}

	public static void UnitedFederation() {
print("           ______");
print("        _-' .   .`-_");
print("    |/ /  .. . '   .\\ \\|");
print("   |/ /            ..\\ \\|");
print(" \\|/ |: .   ._|_ .. . | \\|/");
print("  \\/ |   _|_ .| . .:  | \\/");
print(" \\ / |.   |  .  .    .| \\ /");
print("  \\||| .  . .  _|_   .|||/");
print(" \\__| \\  . :.  .|.  ./ |__/");
print("   __| \\_  .    .. _/ |__");
print("    __|  `-______-'  |__");
print("       -,____  ____,-");
print("         ---'  `---");
print("UNITED FEDERATION OF PLANETS");
	}

	public static void KlingonBirdOfPrey() {
print("                        _------_        _------_");
print("                       / /~~~~~~~\\----/~~~~~~~\\ \\");
print("                    __|_|    /~ _-~~~~-_ ~\\    |_|__");
print("              __--~~____|   |  /________\\  |   |____~~--__");
print("        __--~~__--~~     ~---__\\   ()   /__---~     ~~--__~~--__");
print("     /~~__--~~                  ~--__--~                  ~~--__~~\\");
print("   / /~~                                                        ~~\\ \\");
print(" / /                                                                \\ \\");
print("(0)                                                                  (0)");
	}

}