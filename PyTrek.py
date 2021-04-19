# This is an attempt to port JTrek (in Java) to Python.  JTrek was based on ZTrek in Inform
# which in turn came from C, and is based on Basic, as described below.
#
#//Source: https://ifarchive.org/indexes/if-archiveXgamesXsourceXinform.html
#//ztrek.inf [29-Feb-2000]
#//IFDB entry
#//Super Z Trek, a Z-Machine implementation of the classic Star Trek. Written by John Menichelli,
#//based on Chris Nystrom C port of a BASIC version.
#//!*************************************************************************
#//!**
#//!**  Super Z Trek: Star Trek for the Z Machine
#//!**
#//!**  Ported to Inform by John Menichelli
#//!**
#//!*************************************************************************
#
#//!** The Star Trek game has been around since the dawn of personal computers.
#//!** This version, written in Inform by John Menichelli, is just the latest
#//!** incarnation of this classic game. If you have any questions, comments
#//!** or bug reports, please email them to me at menichel@@0064pixi.com. This
#//!** program and its source code are in the public domain.
#//!**
#//!** This version is based on the C port of an old BASIC program. The C version
#//!** was written by Chris Nystrom and is available from:
#//!**
#//!** http://www.cfi.org/pub/ccn/startrek
#//!**
#//!** You can contact the author of C port at:
#//!**
#//!** Chris Nystrom
#//!** 1013 Prairie Dove Circle
#//!** Austin, Texas  78758
#//!**
#//!** E-Mail: chris@gnu.ai.mit.edu, nystrom@cactus.org, or ccn@cfi.org
#//
#//!** The original Super Star Trek game comes from the book "BASIC Computer
#//!** Games" edited by David Ahl of Creative Computing fame. It was published
#//!** in 1978 by Workman Publishing, 1 West 39 Street, New York, New York,
#//!** and the ISBN is: 0-89489-052-3.
#//!**
#//!** Here is the original BASIC header:
#//!**
#//!** SUPER STARTREK - MAY 16, 1978 - REQUIRES 24K MEMORY
#//!**
#//!**        **** STAR TREK ****        ****
#//!** SIMULATION OF A MISSION OF THE STARSHIP ENTERPRISE,
#//!** AS SEEN ON THE STAR TREK TV SHOW.
#//!** ORIGINAL PROGRAM BY MIKE MAYFIELD, MODIFIED VERSION
#//!** PUBLISHED IN DEC''S "101 BASIC GAMES", BY DAVE AHL.
#//!** MODIFICATIONS TO THE LATTER (PLUS DEBUGGING) BY BOB
#//!** LEEDOM - APRIL & DECEMBER 1974,
#//!** WITH A LITTLE HELP FROM HIS FRIENDS . . .
#//!** COMMENTS, EPITHETS, AND SUGGESTIONS SOLICITED --
#//!** SEND TO:  R. C. LEEDOM
#//!**           WESTINGHOUSE DEFENSE & ELECTRONICS SYSTEMS CNTR.
#//!**           BOX 746, M.S. 338
#//!**           BALTIMORE, MD  21203
#//!**
#//!** CONVERTED TO MICROSOFT 8 K BASIC 3/16/78 BY JOHN BORDERS
#//!** LINE NUMBERS FROM VERSION STREK7 OF 1/12/75 PRESERVED AS
#//!** MUCH AS POSSIBLE WHILE USING MULTIPLE STATMENTS PER LINE
#//!**
#//!** Notes on the Inform version:
#//!**
#//!** Since Inform only works with integers, this version eliminates the
#//!** guesswork involved in moving and firing torpedoes. To make up for
#//!** this, the torpedo algorithm gives the torped a random chance to miss,
#//!** which increases as the range increases.

#import java.util.Scanner;
import sys
from typing import Any
import random

class PyTrek():
	#//!** Constants
	MAX_TORPS = 10;
	KLINGON_POWER = 200;
	MAX_POWER = 3000;
	SCREEN_SIZE = 6;
	ENTERPRISE = 1;
	KLINGON = 2;
	BASE = 3;
	STAR = 4;
	WARP_ENGINES = 0;
	SHORT_RANGE = 1;
	LONG_RANGE = 2;
	PHASER_CONTROL = 3;
	PHOTON_TUBES = 4;
	DAMAGE_CONTROL = 5;
	SHIELD_CONTROL = 6;
	LIBRARY_COMPUTER = 7;

	#//!** Global Variables
	trek_docked_flag = 0;                #//! 1 or 2 if Enterprise is docked
	trek_current_energy = 0;             #//! Current energy
	trek_shield_value = 0;               #//! Current shield value
	trek_torp_capacity = MAX_TORPS;      #//! Photon torpedo capacity
	trek_torps_remaining = 0;            #//! Photon torpedoes left
	trek_max_speed = 0;                  #//! Maximum allowed speed
	trek_end_of_time = 0;                #//! End of time/game
	trek_current_date = 0;               #//! Current stardate
	trek_total_bases = 0;                #//! Total starbases
	trek_total_klingons = 0;             #//! Klingons at start
	trek_klingons_left = 0;              #//! Total Klingons left
	trek_quadrant_position = 0;          #//! These two variables are used
	trek_sector_position = 0;            #//! to calculate the quadrant and
              							 #//! sector location of the Enterprise

	#//!** Arrays
	trek_long_range_galaxy = [];	     #new int[64];	//! Holds long range scan data
	trek_galaxy_history = [];	         #new int[64];  //! Hold history of all long and short range scans
	trek_temp_array = [];	             #new int[64];  //! Used for printing long range scans
	trek_sector = [];	                 #new int[64];  // ! Sector data array
	trek_damage_array = [];              #new int[8];   // ! Damage Array
	trek_klingon_array = [];             #new int[3];  // ! Array used to track Klingon damage;
	
	#//omit for now - I don''t know if these are chars or strings
	#//Array text_array -> 60;                 ! Input array for keyboard entry

	#//! Main Program
	#//[ Main ;
	#public static void main(String[] args) {
   	#	PlayTrek();
	#}
	def main():
		PyTrek.PlayTrek();

	#//[ PlayTrek ;
	def PlayTrek():
   		PyTrek.TrekIntro();
   		PyTrek.Initialize();
   		PyTrek.EndScreen();

	#//[ TrekIntro ;
	def TrekIntro():
   		#//font off;
		print("*************************************");
		print("*                                   *");
		print("*                                   *");
		print("*       * * Super Py Trek * *       *");
		print("*                                   *");
		print("*                                   *");
		print("*************************************");
		print("^^^");
   		#//spaces (0->33)/2 - 12;
   	
		PyTrek.Enterprise();
		Pause();
	#}

	#//[ Initialize i j bases stars klingons;
	def Initialize():
		i=0; 
		j=0;
		bases=0;
		stars=0;
		klingons=0;

   		#//! Initialize time
		PyTrek.trek_current_date = (20 + random_int(10)) * 1000;
		PyTrek.trek_end_of_time = (25 + random_int(10)) * 10;

		PyTrek.InitializeArrays();

  		#//! Setup What Exists in Galaxy
		#for (i = 0; i < 64; i++):
		for i in range(0,64):
			#p("Initialize: i = ");
			#print(i);
			PyTrek.trek_galaxy_history[i] = 999;
		#}

		for i in range(0,64):
			j = random_int(100);
			if j>=98:
				klingons = 3;
			elif j>=95:
				klingons = 2;
			elif j>=81:
				klingons = 1;
			else:
				klingons = 0;
			#}

			PyTrek.trek_klingons_left = PyTrek.trek_klingons_left + klingons;

			if random_int(100) > 96:
				bases = 1;
			else:
				bases = 0;
			#}

			PyTrek.trek_total_bases = PyTrek.trek_total_bases + bases;
			stars = random_int(8);
			PyTrek.trek_long_range_galaxy[i] = (klingons * 100) + (bases * 10) + stars;
   		#} end for

		if (PyTrek.trek_total_bases == 0):
			i = random_int(64);	#// - 1;
			j = PyTrek.trek_long_range_galaxy[i];
			j = j + 10;
			PyTrek.trek_long_range_galaxy[i] = j;
			PyTrek.trek_total_bases + 1;	#++
 		#}

		if (PyTrek.trek_klingons_left > PyTrek.trek_end_of_time // 10):
 			PyTrek.trek_end_of_time = (PyTrek.trek_klingons_left + 1) * 10;
 		#}

		PyTrek.trek_total_klingons = PyTrek.trek_klingons_left;

		#//! Initialize Enterprise
		PyTrek.trek_docked_flag = 0;
		PyTrek.trek_current_energy = PyTrek.MAX_POWER;
		PyTrek.trek_torps_remaining = PyTrek.trek_torp_capacity;
		PyTrek.trek_shield_value = 0;
		PyTrek.trek_max_speed = 8;
		PyTrek.trek_quadrant_position = random_int(64); 
		PyTrek.trek_sector_position = random_int(64); 

		for i in range(0,8):
			PyTrek.trek_damage_array[i] = 5;
		#}

		PyTrek.MissionBrief();
		#//SetScreen();
		PyTrek.NewQuadrant();
		PyTrek.UpdateStatus();
		PyTrek.ShortRangeScan();
		PyTrek.MainMenu();
	#}
	
	def InitializeArrays():
		#make this 65 instead of 64 because sometimes index 64 is used
		for i in range(0,65):
			PyTrek.trek_long_range_galaxy.append(0);		
			PyTrek.trek_galaxy_history.append(0);
			PyTrek.trek_temp_array.append(0);
			PyTrek.trek_sector.append(0);
			
		for i in range(0,8):
			PyTrek.trek_damage_array.append(0); 
			
		for i in range(0,3):
			PyTrek.trek_klingon_array.append(0);
			
		return;
	#end InitializeArrays

	#//[ NewQuadrant i j k b s ;
	def NewQuadrant():
		i=0; j=0; k=0; b=0; s=0;
		PyTrek.trek_galaxy_history[PyTrek.trek_quadrant_position] = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];

		for i in range(0,3):
			PyTrek.trek_klingon_array[i] = PyTrek.KLINGON_POWER;
		#}

		i = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];

		k = i // 100;                     #//! Klingons
		b = i // 10 - (10 * k);           #//! Bases
		s = i - (100 * k) - (10 * b);     #//! Stars

		for i in range (0,64):	#(i = 0; i < 64; i++) {
			PyTrek.trek_sector[i] = 0;
		#}

		print("[NewQuadrant trek_sector "+ str(PyTrek.trek_sector_position)+ " contains the Enterprise]");
		PyTrek.trek_sector[PyTrek.trek_sector_position] = PyTrek.ENTERPRISE;

		print("[NewQuadrant: there are "+str(k)+" Klingons in this quadrant]"); 
		for i in range(0,k):	#(i = 1; i <= k; i++)         //! Position Klingons
			#Retry1: {
			#	j = random_int(64);	// - 1;
			#	if (trek_sector[j] == 0) {
			#	 	break Retry1;
			#	} else {
			#		trek_sector[j] = KLINGON;
			#	}
			#}
			j = random_int(64)
			while (j==0):
				j = random_int(64)
			#}
			PyTrek.trek_sector[j] = PyTrek.KLINGON;
			print("[NewQuadrant: sector "+str(j)+" contains a Klingon]");
		#}

		for i in range (1,b):	#(i = 1; i <= b; i++)         //! Position base
			#Retry2: {
			#	j = random_int(64);	// - 1;
			#	if (trek_sector[j] == 0) {
			#	 	break Retry2;
			#	} else {
			#		trek_sector[j] = BASE;
			#	}
			#}
			j = random_int(64)
			while (j==0):
				j = random_int(64)
			PyTrek.trek_sector[j] = PyTrek.BASE;			
		#}

		for i in range(1,s):  #(i = 1; i <= s; i++)         //! Position stars
			#Retry3: {
			#	j = random_int(64); //- 1;
			#	if (trek_sector[j] == 0) {
			#		break Retry3;
			#	} else {
			#		trek_sector[j] = STAR;
			#	}
			#}
			j = random_int(64)
			while (j==0):
				j = random_int(64)
				
			#added because of IndexError: list assignment index out of range
			print("[NewQuadrant trek_sector j="+str(j)+" is a star]");
			PyTrek.trek_sector[j] = PyTrek.STAR;				
		#}
		return;
	#} end NewQuadrant

#//[ SetScreen i j;
#//   @erase_window $ffff;
#//   @split_window SCREEN_SIZE;
#//   @set_window 1;
#//   style reverse;
#//   j = SCREEN_SIZE;
#//   for (i = 1 : i <= j: i++)
#//   {
#//      @set_cursor i 1;
#//      spaces (0->33)-1;
#//   }
#//   style roman;
#//];

	#//[ MissionBrief ;
	def MissionBrief():
		#//@erase_window $ffff;
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
		print("a total of " + str(PyTrek.trek_klingons_left) + " Klingon battlecruisers in your area.");
		print(" ");
		print("5. Starfleet Operations calculates that it will take");
		print("approximately " + str(PyTrek.trek_end_of_time // 10 ) + " days to mobilize our");
		print("forces and begin sending reinforcements to the front. We need you");
		print("to hold off the invading Klingon fleet until those reinforcements");
		print("arrive.");
		print(" ");
		print("6. Good luck and good hunting.");
		print(" ");
		#//print "[Press any key to accept command]";

		Pause();
		return;
	#} end MissionBrief

	#//[ UpdateStatus i;
	def UpdateStatus():
		#//@set_window 1;

		#//@set_cursor 1 1;
		#//style reverse;
		#//for (i = 1: i <= 2: i++) {
		#//@set_cursor i 1;
		#//spaces (0->33)-1; }

		#//row 1
		#//@set_cursor 1 1;
		curdat: str = str(PyTrek.trek_current_date // 10)+ "." + str(PyTrek.trek_current_date % 10);
		remdat: str = str(PyTrek.trek_end_of_time // 10) + "." + str(PyTrek.trek_end_of_time % 10);
		print("Current Date: "+curdat + "    " + "Days Remaining: "+remdat);

		#//row 2
		print("Klingons Remaining: " + str(PyTrek.trek_klingons_left) + "    " +"Bases Remaining: "+str(PyTrek.trek_total_bases) );

		#//row 3
		enerem: int = PyTrek.trek_current_energy + PyTrek.trek_shield_value;
		print("Shield Value: "+ str(PyTrek.trek_shield_value)+ "    " +"Total Energy Remaining: "+str(enerem));
		return;
	#end UpdateStatus
	
	#//[ MainMenu i ;
	def MainMenu():		
		menu_line1: str = "1: Nav     2: SRS     3: LRS      4: Phaser  5: Torp"
		menu_line2: str = "6: Shield  7: Damage  8: Library  9: Help    0: Quit"

		while(True):
			print(menu_line1);
			print(menu_line2);

			i: int = read_int();
			while(i<0):
				read_int()
			
			if (i==0 or i>9):
				break
			else:
				if i==1:
					PyTrek.CourseControl()
				elif i==2:
					PyTrek.ShortRangeScan()
				elif i==3:
					PyTrek.LongRangeScan()
				elif i==4:
					PyTrek.PhaserControl()
				elif i==5:
					PyTrek.PhotonTorps()
				elif i==6:
					PyTrek.ShieldControl()
				elif i==7:
					PyTrek.DamageControl()
				elif i==8:
					PyTrek.Library()
				elif i==9:
					PyTrek.Help()
				else:
					print("invalid selection "+str(i) );
						
			#//@read_char 1 -> i;

			#switch(i) {
			#	case 0 : break;
			#	case 1 : CourseControl(); break;
			#	case 2 : ShortRangeScan(); break;
			#	case 3 : LongRangeScan(); break;
			#	case 4 : PhaserControl(); break;
			#	case 5 : PhotonTorps(); break;
			#	case 6 : ShieldControl(); break;
			#	case 7 : DamageControl(); break;
			#	case 8 : Library(); break;
			#	case 9 : Help(); break;
			#	default : print("Invalid Command "+i);
			#}
			#if (i == 0) break;
		#}
		return;
	#}

	#//[ CourseControl i course speed;
	def CourseControl(): # {
		print("[CourseControl]");
		i=0;
		course=0;
		speed=0;
		PyTrek.PrintCompass();

		print("^Enter course (1-8): ");
		i = read_int();
		while(i<0):
			i = read_int();

		if (i < 1 or i > 8):
			print("^Lt. Sulu reports: ~Incorrect course data, sir!~ ["+str(i)+"]^");
			return;
		#}

		#//course = i - 48;
		course = i;
		print("Course: "+str(course));

		PyTrek.trek_max_speed = PyTrek.trek_damage_array[PyTrek.WARP_ENGINES];
		PyTrek.trek_max_speed = PyTrek.trek_max_speed + 3;
		print("^^Enter warp speed (1-"+ str(PyTrek.trek_max_speed)+ "): ");
		i = read_int();
		while(i<0):
			i = read_int();   		
		
		#//speed = i - 48;
		speed = i;
		print("Attempting warp "+str(speed));

		if (speed < 1): # {
			print("^Lt. Sulu reports: ~Incorrect speed, sir!~^^");
			return;
		#}

		if (speed > PyTrek.trek_max_speed): # {
			print("^Chief Engineer Scott reports: ~The engines won't take more than warp "+ str(trek_max_speed)+ "!~^^");
			return;
		#}

		if (speed * 10 > PyTrek.trek_current_energy + PyTrek.trek_shield_value): # {
			print("^Chief Engineer Scott reports: ~We don't have enough energy power to go that fast!~^^");
			return;
		#}

		PyTrek.trek_current_energy = PyTrek.trek_current_energy - (speed * 10);

		print("Reaching warp "+ str(speed) + "^^");

		if (PyTrek.trek_current_energy < 0):
		#{
			print("^Diverting Shield Control supplies energy to complete the maneuver.^");

			PyTrek.trek_shield_value = PyTrek.trek_shield_value + PyTrek.trek_current_energy;
			PyTrek.trek_current_energy = 0;

			if (PyTrek.trek_shield_value < 0): # {
				PyTrek.trek_shield_value = 0;
			#}
		#}
		PyTrek.CompleteManeuver(course, speed);
		if (PyTrek.trek_current_energy + PyTrek.trek_shield_value <= 0):
			PyTrek.OutOfEnergy();
		#}
		return;
	#}

	#//[ CompleteManeuver course speed i j xs ys xq yq;
	def CompleteManeuver(course: int, speed: int): # {
		i=0; j=0; xs=0; ys=0; xq=0; yq=0;
		print("[CompleteManeuver("+str(course)+","+str(speed)+")]");
		xs = (PyTrek.trek_sector_position % 8) + 1;
		ys = 8 - (PyTrek.trek_sector_position // 8);

		xq = (PyTrek.trek_quadrant_position % 8) + 1;
		yq = 8 - (PyTrek.trek_quadrant_position // 8);

		j = PyTrek.trek_sector_position;

		#for (i = 1; i <= speed; i++)
		for i in range(1,speed):
		#{
			print("[CompleteManeuver checking OutOfBounds]");
			if (PyTrek.OutOfBounds(course) == 1):
			#{
				print("^Movement aborted - you may not leave your designated patrol area.^");
				break;
			#}

			#switch(course)
			#{
			#	case 1: ys++; break;
			#	case 2: xs++; ys++; break;
			#	case 3: xs++; break;
			#	case 4: xs++; ys--; break;
			#	case 5: ys--; break;
			#	case 6: ys--; xs--; break;
			#	case 7: xs--; break;
			#	case 8: xs--; ys++; break;
			#	default: print("Unable to complete maneuver "+course);
			#}
			
			if (course == 1):
				ys=ys+1; 
			elif (course == 2):
				xs=xs+1; ys=ys+1; 
			elif (course == 3):
				xs=xs+1; 
			elif (course == 4):
				xs=xs+1; ys=ys-1;
			elif (course == 5):
				ys=ys-1; 
			elif (course == 6):
				ys=ys-1; xs=xs-1; 
			elif (course == 7):
				xs=xs-1; 
			elif (course == 8):
				xs=xs-1; ys=ys+1; 
			else:
				print("Unable to complete maneuver "+course); 
			#end if block

			#if (xs < 1 || xs > 8 || ys < 1 || ys > 8):
			if (xs < 1 or xs > 8 or ys < 1 or ys > 8):
				if (xs < 1): 
					xs = 8; xq=xq-1; 
				if (xs > 8): 
					xs = 1; xq=xq+1; 
				if (ys < 1):
					ys = 8; yq=yq-1; 
				if (ys > 8):
					ys = 1; yq=yq+1; 

				j = (8 * (8 - ys)) + xs - 1;
				PyTrek.trek_sector_position = j;
				PyTrek.trek_quadrant_position = (8 * (8 - yq)) + xq - 1;
				if (PyTrek.trek_docked_flag > 0):	# {
					PyTrek.trek_docked_flag = 0;
				#end if
				PyTrek.NewQuadrant();
			#}
			else:
				j = (8 * (8 - ys)) + xs - 1;

				if (PyTrek.trek_sector[j] == PyTrek.KLINGON):
					print ("^Movement aborted to avoid collision with Klingon vessel.^");
					break;
				elif (PyTrek.trek_sector[j] == PyTrek.STAR): 
				#{
					print ("^Movement aborted to avoid collision with star.^");
					break;
				#}
				#//! You can pass through a base
				if (PyTrek.trek_sector[j] == PyTrek.BASE):
				#{
					if (i == speed):
					#{
						print ("^The Enterprise is now docked.^");
						PyTrek.trek_docked_flag = 1;
						PyTrek.trek_sector[PyTrek.trek_sector_position] = 0;
						PyTrek.trek_sector_position = j;
						#// jump DoneMoving;
						DoneMoving(speed);
					#}
					else:
						continue;
					#}
				#}
				else:
				#{
					PyTrek.trek_sector[j] = PyTrek.ENTERPRISE;
					if (PyTrek.trek_docked_flag > 0):
					#{
						PyTrek.trek_docked_flag = 0;
						PyTrek.trek_sector[PyTrek.trek_sector_position] = PyTrek.BASE;
					#}
					else:
					#{
						PyTrek.trek_sector[PyTrek.trek_sector_position] = 0;
					#}
					PyTrek.trek_sector_position = j;
				#}
			#}
		#}
		return;
	#}
	#//!.DoneMoving;

	def DoneMoving(speed: int):
		print("[DoneMoving("+speed+")]");
		PyTrek.trek_current_date = PyTrek.trek_current_date + speed;
		PyTrek.trek_end_of_time = PyTrek.trek_end_of_time - speed;
		if (PyTrek.trek_end_of_time <= 0): # {
			EndOfTime();
		#}
		PyTrek.UpdateStatus();
		PyTrek.DamageRepair();
		PyTrek.UpdateStatus();
		PyTrek.ShortRangeScan();
		return;
	#}

	# OutOfBounds.  This is boolean, but returns 0 or 1
	#//[ OutOfBounds course xs ys xq yq;
	def OutOfBounds(course: int) -> int: 
		print("[OutOfBounds("+str(course)+")]");
		if (course<1 or course>8): # {
			print("Invalid course: "+course);
			return 0;
		#}
		xs = 0; ys = 0; xq = 0; yq = 0;
		xs = (PyTrek.trek_sector_position % 8) + 1;
		ys = 8 - (PyTrek.trek_sector_position // 8);

		xq = (PyTrek.trek_quadrant_position % 8) + 1;
		yq = 8 - (PyTrek.trek_quadrant_position // 8);

		if (xq == 1 and yq == 1 and xs == 1 and ys == 1): # //! Lower left corner
		#{
			#//if (course == 4 or 5 or 6 or 7 or 8)
			if (course > 3):
				return 1;
			else:
				return 0;
		#}

		if (xq == 8 and yq == 8 and xs == 8 and ys == 8): #//! Upper right corner
		#{
			#//if (course == 1 or 2 or 3 or 4 or 8)
			if (course < 5 or course==8):
				return 1;
			else:
				return 0;
		#}

		if (xq == 8 and yq == 1 and xs == 8 and ys == 1): # //! Lower right corner
		#{
			#//if (course == 2 or 3 or 4 or 5 or 6)
			if (course > 1 and course < 7 ):
				return 1;
			else:
				return 0;
		#}

		if (xq == 1 and yq == 8 and xs == 1 and ys == 8): #//! Upper left corner
		#{
			#//if (course == 1 or 2 or 6 or 7 or 8)
			if (course <3 or course > 5):
				return 1;
			else:
				return 0;
		#}

		if (xq == 1 and xs == 1):	# //! Left edge
		#{
			#//if (course == 6 or 7 or 8)
			if (course > 5):
				return 1;
			else:
				return 0;
		#}

		if (xq == 8 and xs == 8): # //! Right Edge
		#{
			#//if (course == 2 or 3 or 4)
			if (course > 1 and course < 5):
				return 1;
			else:
				return 0;
		#}

		if (yq == 8 and ys == 8): #//! Top edge
		#{
			#//if (course == 1 or 2 or 8)
			if (course < 3 or course == 8):
				return 1;
			else:
				return 0;
		#}

		if (yq == 1 and ys == 1): # //! Bottom edge
		#{
			#//if (course == 4 or 5 or 6)
			if (course > 3 and course < 7):
				return 1;
			else:
				return 0;
		#}

		return 0;
	#}
	#end OutOfBounds

	#//[ PrintCompass ;
	def PrintCompass():
		new_line();
		print(" 8  1  2");
		print("  \\ | / ");		#//make backslash double
		print("7  -+-  3");
		print("  / | \\ ");
		print(" 6  5  4");
	#}

	#//[ ShortRangeScan x y ;
	def ShortRangeScan():	# {
		print("[ShortRangeScan]");
		x=0; y=0;
		if (PyTrek.trek_damage_array[PyTrek.SHORT_RANGE] < 5): # {
			print ("^Short Range Sensors are inoperative.^");
		#}

		#//! Determine Quadrant

		x = (PyTrek.trek_quadrant_position % 8) + 1;
		y = 8 - (PyTrek.trek_quadrant_position // 8);

		print ("^Short range scan of quadrant ");
		p(str(x) + ", " + str(y) + " (");
		#//PrintQuadrantName(x, y);
		p( PyTrek.QuadrantName(x,y) );
		print(")^^");

		print ("     1   2   3   4   5   6   7   8^");
		print ("    --- --- --- --- --- --- --- ---^");
		#//for (x = 0; x < 64; x++)
		for x in range(0,64):
		#{
			if (x % 8 == 0):
			#{
				p( " ");
				p( (8 - (x//8)) );
				p(":");
		#}

			#switch (trek_sector[x])
			#{
			#   case 0 : p( "  . "); break;
			#   case 1 : p(" +E+"); break;
			#   case 2 : p(" +K+"); break;
			#   case 3 : 	if (trek_docked_flag == 0) { p(" >B<");}
			#				else { p(" >D<");}
			#				break;
			#      case 4 : p("  # "); break;
			#      default: p(" ");
			#   }
			ts: int = PyTrek.trek_sector[x];
			if (ts==0):
				p( "  . ");
			elif (ts==PyTrek.ENTERPRISE):	#1
				p(" +E+");
			elif (ts==PyTrek.KLINGON):		#2
				p(" +K+");
			elif (ts==PyTrek.BASE):			#3
				if (trek_docked_flag == 0): 
					p(" >B<");
				else:
					p(" >D<");
			elif (ts==PyTrek.STAR):			#4
				p("  # ");
			else:
				p(" ");
			
			if ((x + 1) % 8 == 0): # {
				print ("^");
			#}
		#}

		y = 0;
		#for (x = 1; x < 64; x++) {
		for x in range(1,64):
			if (PyTrek.trek_sector[x] == 2): 
				y=y+1;
		#}
		p("^Alert Condition: ");

		if (y > 0):
			print ("Red^");
		else:
			if (PyTrek.trek_current_energy * 10 < PyTrek.MAX_POWER):
				print ("Yellow^");
			else:
				print ("Green^");

		print("[returning from ShortRangeScane]");				
		return;
	#}	//end ShortRangeScan

	#//[ LongRangeScan i j temp_pos;
	#public static void LongRangeScan() {
	def LongRangeScan():
		i=0; j=0; temp_pos=0;
		print("[LongRangeScan]");
		if (PyTrek.trek_damage_array[PyTrek.LONG_RANGE] < 5): # {
			print("^Long Range Sensors are inoperative.^");
		#}

		for i in range(0,64):
			PyTrek.trek_temp_array[i] = 999;

		temp_pos = PyTrek.trek_quadrant_position;

		if (temp_pos == 0):	#   //! Upper left
		#{
			PyTrek.trek_temp_array[0] = PyTrek.trek_long_range_galaxy[0];
			PyTrek.trek_temp_array[1] = PyTrek.trek_long_range_galaxy[1];
			PyTrek.trek_temp_array[8] = PyTrek.trek_long_range_galaxy[8];
			PyTrek.trek_temp_array[9] = PyTrek.trek_long_range_galaxy[9];

			PyTrek.trek_galaxy_history[0] = PyTrek.trek_long_range_galaxy[0];
			PyTrek.trek_galaxy_history[1] = PyTrek.trek_long_range_galaxy[1];
			PyTrek.trek_galaxy_history[8] = PyTrek.trek_long_range_galaxy[8];
			PyTrek.trek_galaxy_history[9] = PyTrek.trek_long_range_galaxy[9];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos == 7): #   //! Upper right
		#{
			PyTrek.trek_temp_array[6]  = PyTrek.trek_long_range_galaxy[6];
			PyTrek.trek_temp_array[7]  = PyTrek.trek_long_range_galaxy[7];
			PyTrek.trek_temp_array[14] = PyTrek.trek_long_range_galaxy[14];
			PyTrek.trek_temp_array[15] = PyTrek.trek_long_range_galaxy[15];

			PyTrek.trek_galaxy_history[6]  = PyTrek.trek_long_range_galaxy[6];
			PyTrek.trek_galaxy_history[7]  = PyTrek.trek_long_range_galaxy[7];
			PyTrek.trek_galaxy_history[14] = PyTrek.trek_long_range_galaxy[14];
			PyTrek.trek_galaxy_history[15] = PyTrek.trek_long_range_galaxy[15];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos == 56): #  //! Lower left
		#{
			PyTrek.trek_temp_array[48] = PyTrek.trek_long_range_galaxy[48];
			PyTrek.trek_temp_array[49] = PyTrek.trek_long_range_galaxy[49];
			PyTrek.trek_temp_array[56] = PyTrek.trek_long_range_galaxy[56];
			PyTrek.trek_temp_array[57] = PyTrek.trek_long_range_galaxy[57];

			PyTrek.trek_galaxy_history[48] = PyTrek.trek_long_range_galaxy[48];
			PyTrek.trek_galaxy_history[49] = PyTrek.trek_long_range_galaxy[49];
			PyTrek.trek_galaxy_history[56] = PyTrek.trek_long_range_galaxy[56];
			PyTrek.trek_galaxy_history[57] = PyTrek.trek_long_range_galaxy[57];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos == 63): #  //! Lower right
		#{
			PyTrek.trek_temp_array[54] = PyTrek.trek_long_range_galaxy[54];
			PyTrek.trek_temp_array[55] = PyTrek.trek_long_range_galaxy[55];
			PyTrek.trek_temp_array[62] = PyTrek.trek_long_range_galaxy[62];
			PyTrek.trek_temp_array[63] = PyTrek.trek_long_range_galaxy[63];

			PyTrek.trek_galaxy_history[54] = PyTrek.trek_long_range_galaxy[54];
			PyTrek.trek_galaxy_history[55] = PyTrek.trek_long_range_galaxy[55];
			PyTrek.trek_galaxy_history[62] = PyTrek.trek_long_range_galaxy[62];
			PyTrek.trek_galaxy_history[63] = PyTrek.trek_long_range_galaxy[63];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos < 8): #    //! Top edge
		#{
			PyTrek.trek_temp_array[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_temp_array[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_temp_array[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_temp_array[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
			PyTrek.trek_temp_array[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_temp_array[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];

			PyTrek.trek_galaxy_history[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_galaxy_history[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_galaxy_history[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_galaxy_history[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
			PyTrek.trek_galaxy_history[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_galaxy_history[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos > 55): #   //! Bottom edge
		#{
			PyTrek.trek_temp_array[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_temp_array[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_temp_array[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_temp_array[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
			PyTrek.trek_temp_array[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_temp_array[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];

			PyTrek.trek_galaxy_history[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_galaxy_history[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_galaxy_history[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_galaxy_history[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
			PyTrek.trek_galaxy_history[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_galaxy_history[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		if (temp_pos % 8 == 0):  #//! Left edge
		#{
			PyTrek.trek_temp_array[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_temp_array[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_temp_array[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_temp_array[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
			PyTrek.trek_temp_array[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_temp_array[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];

			PyTrek.trek_galaxy_history[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_galaxy_history[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_galaxy_history[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_galaxy_history[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
			PyTrek.trek_galaxy_history[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
			PyTrek.trek_galaxy_history[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}
		if ((temp_pos+1) % 8 == 0):  #//! Right edge
		#{
			PyTrek.trek_temp_array[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_temp_array[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_temp_array[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_temp_array[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
			PyTrek.trek_temp_array[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_temp_array[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];

			PyTrek.trek_galaxy_history[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
			PyTrek.trek_galaxy_history[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
			PyTrek.trek_galaxy_history[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
			PyTrek.trek_galaxy_history[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
			PyTrek.trek_galaxy_history[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
			PyTrek.trek_galaxy_history[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];

			#//jump Printit;
			PyTrek.PrintLongRangeScanResults();
			return;
		#}

		#//! Everything else
		PyTrek.trek_temp_array[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
		PyTrek.trek_temp_array[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];
		PyTrek.trek_temp_array[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
		PyTrek.trek_temp_array[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
		PyTrek.trek_temp_array[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
		PyTrek.trek_temp_array[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
		PyTrek.trek_temp_array[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
		PyTrek.trek_temp_array[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
		PyTrek.trek_temp_array[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];

		PyTrek.trek_galaxy_history[temp_pos]     = PyTrek.trek_long_range_galaxy[temp_pos];
		PyTrek.trek_galaxy_history[(temp_pos-9)] = PyTrek.trek_long_range_galaxy[(temp_pos-9)];
		PyTrek.trek_galaxy_history[(temp_pos-8)] = PyTrek.trek_long_range_galaxy[(temp_pos-8)];
		PyTrek.trek_galaxy_history[(temp_pos-7)] = PyTrek.trek_long_range_galaxy[(temp_pos-7)];
		PyTrek.trek_galaxy_history[(temp_pos-1)] = PyTrek.trek_long_range_galaxy[(temp_pos-1)];
		PyTrek.trek_galaxy_history[(temp_pos+1)] = PyTrek.trek_long_range_galaxy[(temp_pos+1)];
		PyTrek.trek_galaxy_history[(temp_pos+7)] = PyTrek.trek_long_range_galaxy[(temp_pos+7)];
		PyTrek.trek_galaxy_history[(temp_pos+8)] = PyTrek.trek_long_range_galaxy[(temp_pos+8)];
		PyTrek.trek_galaxy_history[(temp_pos+9)] = PyTrek.trek_long_range_galaxy[(temp_pos+9)];
		PyTrek.PrintLongRangeScanResults();

	#}	//end LongRangeScan

	#//.Printit;
	#public static void PrintLongRangeScanResults() {
	def PrintLongRangeScanResults(): 
		print("[PrintLongRangeScanResults]");
		i=0; j=0;
		new_line();
		new_line();

		print ("                 Long Range Scan Results^^");
		print ("      1     2     3     4     5     6     7     8^");
		print ("    ----- ----- ----- ----- ----- ----- ----- -----^");

		#//for (i = 0; i < 64; i++)
		for i in range(0,64):
		#{
			if (i%8 == 0):
			#{
				p( " ");
				p( 8 - i//8);
				p(":");
			#}

			j = PyTrek.trek_temp_array[i];

			p(" ");

			#//if (i == temp_pos)
			#//   style reverse;
			#//else
			#//   style roman;

			#//switch(j)
			#//{
			#//   0 to 9   : print " 00"; print j;
			#//   10 to 98 : print " 0";  print j;
			#//   999      : print " ***";
			#//   default  : print " "; print j;
			#//}
			if (j<10): #{
				p(" 00"); p(j);
			elif (j>9 and j<100): # {	//what about 99 - is that special
				p(" 0");  p( j);
			elif (j==999): # {
				p(" ***");
			else: # {
				p(" "); p(j);
			#}

			p(" ");

			#//style roman;

			if (i%8 == 7): # {
				print( "^");
			#}
		#}
		print("[returning from PrintLongRangeScanResults]");
		return;
	#}

	#//[ TextToNumber n x len mul tot;
	#//This is only called twice, in phaser control and shield control
	#//in both cases, it looks like a single digit number will suffice
	#//public static int TextToNumber() {
	#//	char c = read_char();
	#//	return (int)(c-48);
	#//}
    #//text_array -> 0 = 60;
    #//read text_array 0;

    #//if (text_array->1 > 4)
    #//   return -1;

    #//x = 0;
    #//len = text_array->1;

    #//if (len == 4) mul=1000;
    #//if (len == 3) mul=100;
    #//if (len == 2) mul=10;
    #//if (len == 1) mul=1;

    #//tot = 0;

    #//for (n = 0: n < len: n++)
    #//{
    #//   if (text_array->(n+2) > 47 && text_array->(n+2) < 58)
    #//   {
    #//      x = text_array->(n+2);
    #//      x = x - 48;
    #//      tot = tot + mul * x;
    #//      mul = mul/10;
    #//   }
    #//   else
    #//      return -1;
    #//}
    #//return tot;
	#//];	//end TextToNumber

	#//[ PhaserControl i j k x1 y1 x2 y2 z rng dmg;
	def PhaserControl():
		#public static void PhaserControl() {
		i=0; j=0; k=0; x1=0; y1=0; x2=0; y2=0; z=0; rng=0; dmg=0;
		print("[PhaserControl]");

		if (PyTrek.trek_damage_array[PyTrek.PHASER_CONTROL] < 5): # {
			print("^Science Officer Spock reports: ~Phasers are inoperative, Captain.~^");
			return;
		#}

		k = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];

		k = k // 100;                    #// ! Klingons

		if (k == 0): # {
			print("^Science Officer Spock reports: ~Sensors show no enemy ships in this quadrant~^");
			return;
		#}

		if (PyTrek.trek_damage_array[PyTrek.LIBRARY_COMPUTER] < 5): # {
			print ("^Science Officer Spock reports: ~Computer failure will hamper accuracy, Captain.~^");
			return;
		#}

		print ("^Phasers locked on target. Energy available = " + str(PyTrek.trek_current_energy + PyTrek.trek_shield_value) );

		print ("^Enter number of units to fire: ");

		#//i = TextToNumber();
		i = read_int();
		# a negative number is ok and means aborted

		if (i <= 0):	# {
			print ("^Science Officer Spock reports: ~Phaser fire aborted.~^");
			return;
		#}

		if (i > PyTrek.trek_current_energy): # {
			print("^Science Officer Spock reports: ~Insufficient energy for that attack.~^");
			return;
		#}

		PyTrek.trek_current_energy = PyTrek.trek_current_energy - i;

		if (PyTrek.trek_damage_array[PyTrek.LIBRARY_COMPUTER] < 5): # { //! Computer damage affects targeting
			i = i * PyTrek.trek_damage_array[PyTrek.LIBRARY_COMPUTER] // 5;
		#}

		i = i // k; #//! Divide the energy between each target

		x1 = (PyTrek.trek_sector_position % 8) + 1;
		y1 = 8 - (PyTrek.trek_sector_position // 8);

		k = -1;

		#//for (j = 0; j < 64; j++)
		for j in range(0,64):
		#{
			if (PyTrek.trek_sector[j] == PyTrek.KLINGON):
			#{
				k=k+1;
				x2 = (j % 8) + 1;
				y2 = 8 - (j // 8);

				rng = PyTrek.RangeTrek(x1, y1, x2, y2);

				dmg = i;

				dmg = dmg * 10 // (rng + random_int(5));	#// - 1);

				z = PyTrek.trek_klingon_array[k];

				if (dmg <= 0): # {
					print("^Science Officer Spock reports: ~Sensors show no damage to");
					print("the Klingon battlecruiser at " + str(x2) + ", " + str(y2) + ".~^");
				#}

				if (dmg >= z): 
				#{
					print("^Science Officer Spock reports: ~The Klingon battlecruiser");
					print("at " + str(x2) + ", " + str(y2) + " has been destroyed.~^");
					PyTrek.trek_klingon_array[k] = 0;
					PyTrek.trek_sector[j] = 0;
					PyTrek.trek_klingons_left = PyTrek.trek_klingons_left-1;
					if (PyTrek.trek_klingons_left == 0): # {
						PyTrek.WonGame();
					#}

					z = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];
					z = z - 100;
					PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position] = z;
					if (z // 100 == 0): # {
						PyTrek.ShortRangeScan();
					#}
					PyTrek.UpdateStatus();
				#}
				else:
				#{
					z = z - dmg;
					PyTrek.trek_klingon_array[k] = z;
					print("^Science Officer Spock reports: ~Sensors show that the Klingon");
					print("battlecruiser at " + str(x2) + ", " + str(y2) + " suffered a " + str(dmg) + " unit hit.~^");
				#} //end else
			#}	//end if trek_sector
		#} //end for
		PyTrek.KlingonsShoot();
		print("[returning from PhaserControl]");
		return;
	#}	//end phaser control

	#//[ PhotonTorps course i x1 y1 x2 y2 z index ;
	def PhotonTorps(): # {
		course=0; i=0; x1=0; y1=0; x2=0; y2=0; z=0; index=0;
		print("[PhotonTorps]");
		i2=0;

		if (PyTrek.trek_torps_remaining == 0): # {
			print("^Ensign Chekov reports: ~All photon torpedoes expended, sir!~^");
			return;
		#}

		if (PyTrek.trek_damage_array[PyTrek.PHOTON_TUBES] < 5): # {
		   print("^Ensign Chekov reports: ~Photon torpedo tubes not operational, sir!~^");
		   return;
		#}

		i = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];

		i = i // 100;                    #// ! Klingons

		if (i == 0): # {
			print("^Ensign Chekov reports: ~There are no Klingons in this quadrant, sir!~^");
			return;
		#}

		PyTrek.trek_torps_remaining=PyTrek.trek_torps_remaining-1;
		x1 = (PyTrek.trek_sector_position % 8) + 1;
		y1 = 8 - (PyTrek.trek_sector_position // 8);

		PyTrek.PrintCompass();

		print ("^Enter torpedo course (1-8): ");

		i2 = read_int();	#// 1 -> i;

		if (i2 < 1 or i2 > 8): # {
			print("^Ensign Chekov reports: ~Incorrect course data ["+str(i2)+"], sir!~^");
			return;
		#}

		#//course = c - 48;
		course = i2;

		print (str(course) + "^");

		#for (i = 1; i < 8; i++)
		for i in range(1,8):
		#{
			#switch(course)
			#{
		    #     case 1: y1++; break;
		    #     case 2: x1++; y1++; break;
		    #     case 3: x1++; break;
		    #     case 4: x1++; y1--; break;
		    #     case 5: y1--; break;
		    #     case 6: y1--; x1--; break;
		    #     case 7: x1--; break;
		    #     case 8: x1--; y1++; break;
		    #     default: print("Incorrect course "+course);
			#}
			if course==1:
				y1=y1+1; 
			elif course==2:
				x1=x1+1; y1=y1+1; 
			elif course==3:
				x1=x1+1;
			elif course==4:
				x1=x1+1; y1=y1-1;
			elif course==5:
				y1=y1-1; 
			elif course==6:
				y1=y1-1; x1=x1-1;
			elif course==7:
				x1=x1-1; 
			elif course==8:
				 x1=x1-1; y1=y1+1; 
			else:
				print("Incorrect course: "+str(course));
				return

			if (x1 < 1 or x1 > 8 or y1 < 1 or y1 > 8):
			#{
				print ("^Ensign Chekov reports: ~The torpedo missed, sir!~^");
				break;
			#}

			index = (8 * (8 - y1)) + x1 - 1;

			if (PyTrek.trek_sector[index] == PyTrek.KLINGON):
			#{
				x2 = (PyTrek.trek_sector_position % 8) + 1;
				y2 = 8 - (PyTrek.trek_sector_position // 8);

				z = PyTrek.RangeTrek(x1, y1, x2, y2);

				z = z // 15;

				#//if (random(10) - 1 < z)
				if (random_int(10) < z):
				#{
					print ("^Ensign Chekov reports: ~The torpedo missed, sir!~^");
					break;
				#}
				else:
				#{
					PyTrek.trek_sector[index] = 0;
					PyTrek.trek_klingons_left = PyTrek.trek_klingons_left-1;
					if (PyTrek.trek_klingons_left == 0): # {
						WonGame();
					#}
					z = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];
					z = z - 100;
					PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position] = z;
					print ("^Ensign Chekov reports: ~The Klingon battlecruiser in ");
					print ("sector " + str(x2) + ", " + str(y2) + " has been destroyed, sir!~^");
					PyTrek.UpdateStatus();
					PyTrek.ShortRangeScan();
					break;
				#}
			#}

			if (PyTrek.trek_sector[index] == PyTrek.BASE):
				#{
				print ("^Ensign Chekov reports: ~You destroyed a base, sir!~^");
				PyTrek.trek_total_bases = PyTrek.trek_total_bases - 1;
				z = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];
				z = z - 10;
				PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position] = z;

				if (PyTrek.trek_total_bases == 0 and
					PyTrek.trek_klingons_left <= (PyTrek.trek_current_date // 10) -
					PyTrek.trek_end_of_time // 10):
				#{
					print ("That does it, Captain!! You are hereby relieved of command");
					print ("and sentenced to 99 stardates of hard labor on Cygnus 12!! ");
					PyTrek.LoseGame();
				#}

				if (PyTrek.trek_docked_flag > 0): # //! Undock
				#{
					PyTrek.trek_docked_flag = 0;
					PyTrek.trek_sector[PyTrek.trek_sector_position] = PyTrek.ENTERPRISE;
					PyTrek.ShortRangeScan();
				#}

				break;
			#}

			if (PyTrek.trek_sector[index] == PyTrek.STAR):
			#{
				print ("^Ensign Chekov reports: ~The star absorbed the torpedo's energy, sir!~^");
				break;
			#}
		#}
		PyTrek.KlingonsShoot();
		print("[returning from PhotonTorps]");
		return;
	#}	//end PhotonTorps

	#//[ DamageControl ;
	def DamageControl(): # {
		print("[DamageControl]");
		new_line();
		new_line();
		print ("System                    Status^");
		print ("-------------------------------------^");

		p ("Warp Engines              ");
		if (PyTrek.trek_damage_array[PyTrek.WARP_ENGINES] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Short Range Sensors       ");
		if (PyTrek.trek_damage_array[PyTrek.SHORT_RANGE] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Long Range Sensors        ");
		if (PyTrek.trek_damage_array[PyTrek.LONG_RANGE] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Phaser Control            ");
		if (PyTrek.trek_damage_array[PyTrek.PHASER_CONTROL] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Photon Torpedo Tubes      ");
		if (PyTrek.trek_damage_array[PyTrek.PHOTON_TUBES] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Damage Control            ");
		if (PyTrek.trek_damage_array[PyTrek.DAMAGE_CONTROL] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Shield Control            ");
		if (PyTrek.trek_damage_array[PyTrek.SHIELD_CONTROL] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		p ("Library-Computer          ");
		if (PyTrek.trek_damage_array[PyTrek.LIBRARY_COMPUTER] == 5):
			print ("Operational^");
		else:
			print ("Damaged^");

		new_line();
		return;
	#} //end DamageControl


	#//[ ShieldControl i;
	def ShieldControl(): # {
		i=0;
		print("[ShieldControl]");
		if (PyTrek.trek_damage_array[PyTrek.SHIELD_CONTROL] < 5): # {
			print("Shield Control is inoperative.");
		#}

		print ("^Total energy available = " + str(PyTrek.trek_current_energy + PyTrek.trek_shield_value) );

		print ("^Input number of units to shields: ");

		#//i = TextToNumber();
		i = read_int();
		while (i<0):
			i = read_int();

		if (i == -1): # {
			print ("^Shield Control reports: ~Invalid request - shields unchanged.~^");
			return;
		#}

		if (i == PyTrek.trek_shield_value): # {
			print("^<Shields Unchanged>^");
			return;
		#}

		if (i >= PyTrek.trek_current_energy + PyTrek.trek_shield_value): # {
			print("^Shield Control reports: ~There is insufficient energy available - shields unchanged.~^");
			return;
		#}

		PyTrek.trek_current_energy = PyTrek.trek_current_energy + PyTrek.trek_shield_value - i;
		PyTrek.trek_shield_value = i;

		print ("^Shield Control reports: ~Shields now at " + str(PyTrek.trek_shield_value) + " units per your command.~^");
		PyTrek.UpdateStatus();
		return;
	#}	//end ShieldControl


	#//[ Library i;
	def Library(): # {
		i = 0;
		print("[Library]");
		if (PyTrek.trek_damage_array[PyTrek.LIBRARY_COMPUTER] < 5): # {
			print("^The Library Computer is inoperative.^");
		#}

		print ("^Choose which library-computer function you wish to use:^^");
		print ("1: Galactic Record^");
		print ("2: Status Report^");
		print ("3: Exit^^");
		print ("Enter choice: ");

		i = read_int();	#//@read_char 1 -> i;

		#//System.out.println("(choice='"+i+"')");
		#switch(i)
		#{
		#   case 1 : GalacticRecord(); break;
		#   case 2 : StatusReport(); break;
		#   case 3 : print("^Library-computer exited.^^"); break;
		#   default: print("^Invalid choice.^ '"+i+"'");
		#}
		if i==1:
			PyTrek.GalacticRecord();
		elif i==2:
			PyTrek.StatusReport();
		else:
			print("^Library-computer exited.^^")
		return;
	#} //end Library


	#//[ GalacticRecord i j;
	#//can this be combined with PrintLongRangeScanResults?
	def GalacticRecord(): # {
		i=0; j=0;
		print("[GalacticRecord]");
		new_line();
		new_line();

		print ("                        The Galaxy^^");
		print ("      1     2     3     4     5     6     7     8^");
		print ("    ----- ----- ----- ----- ----- ----- ----- -----^");

		#for (i = 0; i < 64; i++)
		for i in range(0,64):
		#{
			if (i%8 == 0):
			#{
				p(" ");
				p(8 - i//8);
				p(":");
			#}

			j = PyTrek.trek_galaxy_history[i];

			#//if (i == trek_quadrant_position)
			#//	style reverse;
			#//else
			#//	style roman;
			if (i == PyTrek.trek_quadrant_position):
				p("!");
			else: 
				p (" ");

			#//switch(j)
			#//{
			#//	0 to 9   : print " 00"; print j;
			#//	10 to 98 : print " 0";  print j;
			#//	999      : print " ***";
			#//	default  : print " "; print j;
			#//}

			if (j<10): # {
				p(" 00"); p(j);
			elif (j>9 and j<100): # {	//what about 99 - is that special
				p(" 0");  p( j);
			elif (j==999): # {
				p(" ***");
			else: # {
				p(" "); p(j);
			#}
			if (i == PyTrek.trek_quadrant_position):
				p("!");
			else: #{ 
				p (" ");
			#}

			#//style roman;

			if (i%8 == 7): # {
				print ("^");
			#}
		#}
		return;
	#}	//end Galactic Record

	#//[ StatusReport i j x y;
	def StatusReport(): # {
		i=0; j=0; x=0; y=0;
		print("[StatusReport]");
		for i in range(1,64):
		#for (i = 1; i < 64; i++) {
			if (PyTrek.trek_sector[i] == PyTrek.KLINGON): 
				j=j+1;
		#}

		print ("^Status Report:^^");

		stardate: str = str(PyTrek.trek_current_date // 10) + "." + str(PyTrek.trek_current_date % 10);
		print ("Stardate: " + stardate + "^^");

		remdate: str = str(PyTrek.trek_end_of_time // 10) + "." + str(PyTrek.trek_end_of_time % 10); 
		print ("Time remaining in mission: " + remdate + " days^^");

		x = (PyTrek.trek_quadrant_position % 8) + 1;
		y = 8 - (PyTrek.trek_quadrant_position // 8);

		print ("Position:^^");
		p ("   Quadrant: " + str(x) + ", " + str(y) + " (");
		#//PrintQuadrantName(x, y);
		p( PyTrek.QuadrantName(x,y));
		print (")^^");

		x = (PyTrek.trek_sector_position % 8) + 1;
		y = 8 - (PyTrek.trek_sector_position // 8);

		print ("   Sector:   " +  str(x) + ", " + str(y) + "^^");

		p ("Alert Condition: ");

		if (j > 0):
			print ("Red^^");
		elif (PyTrek.trek_current_energy * 10 < PyTrek.MAX_POWER):
			 print ("Yellow^^");
		else:
			 print ("Green^^");

		print ("Klingon warships remaining: " + str(PyTrek.trek_klingons_left) + "^^");

		print ("Total bases remaining: " + str(PyTrek.trek_total_bases) + "^^");

		energ: int = PyTrek.trek_current_energy + PyTrek.trek_shield_value
		print ("Total energy remaining: " + str(energ) + "^^");

		print ("Current shield setting: " + str(PyTrek.trek_shield_value) + "^^");

		print ("Total torpedoes remaining: " + str(PyTrek.trek_torps_remaining) + "^");
		return;
	#}	//end StatusReport

	#//[ KlingonsShoot i j k x1 y1 x2 y2 rng dmg;
	def KlingonsShoot(): # {
		i=0; j=0; k=0; x1=0; y1=0; x2=0; y2=0; rng=0; dmg=0;
		print("[KlingonsShoot]");

		i = PyTrek.trek_long_range_galaxy[PyTrek.trek_quadrant_position];

		i = i // 100;                     #//! Klingons

		if (i == 0): return;

		if (PyTrek.trek_docked_flag > 0): # {
			print("^Starbase shields protect the Enterprise^^");
			return;
		#}

		j = -1;
		#for (k = 0; k < 64; k++)
		for k in range(0,64):
		#{
			if (PyTrek.trek_sector[k] == PyTrek.KLINGON):
			#{
				j=j+1;
				x1 = (k % 8) + 1;
				y1 = 8 - (k // 8);

				x2 = (PyTrek.trek_sector_position % 8) + 1;
				y2 = 8 - (PyTrek.trek_sector_position // 8);

				rng = PyTrek.RangeTrek(x1, y1, x2, y2);

				dmg = PyTrek.trek_klingon_array[j];

				x2 = PyTrek.trek_klingon_array[j];

				x2 = x2 * 2 // 3; #//! Reduce available Klingon energy by 1/3

				PyTrek.trek_klingon_array[j] = x2;

				dmg = dmg * 10 // (rng + random_int(5) );	#// - 1);

				print ("^The Klingon battlecruiser at " + x1 + ", " + y1 +
					" fires on you for " + dmg + " units of damage.^");

				if (dmg > trek_shield_value):
				#{
					PyTrek.ShipDestroyed();
				#}
				else:
				#{
					PyTrek.trek_shield_value = PyTrek.trek_shield_value - dmg;
					print ("^Shield energy is down to " + PyTrek.trek_shield_value + " units.^");
					if (dmg >= 20):
					#{
						#this is complicated
						#if (random_int(10) < 7 || (dmg * 10 // PyTrek.trek_shield_value > 2))
						if ( (random_int(10) < 7) or ( (dmg * 10 // PyTrek.trek_shield_value) > 2) ):
						#{
							dmg = random_int(8);	#// - 1;
							if (PyTrek.trek_damage_array[dmg] > 0):
							#{
								x2 = PyTrek.trek_damage_array[dmg];
								x2=x2-1;
								PyTrek.trek_damage_array[dmg] = x2;
							#}
							print ("^Damage control reports: ~");
							#switch(dmg)
							#{
							#	case 0 :  p("The warp engines were"); break;
							#	case 1 :  p("The short range sensors were"); break;
							#	case 2 :  p("The long range sensors were"); break;
							#	case 3 :  p("Phaser controls were"); break;
							#	case 4 :  p("The photon torpedo tubes were"); break;
							#	case 5 :  p("Damage control was"); break;
							#	case 6 :  p("Shield control was"); break;
							#	case 7 :  p("The library-computer was"); break;
							#	default:
							#}
							if dmg==0:
								p("The warp engines were");
							elif dmg==1:
								p("The short range sensors were");
							elif dmg==2:
								p("The long range sensors were");
							elif dmg==3:
								p("Phaser controls were");
							elif dmg==4:
								p("The photon torpedo tubes were");
							elif dmg==5:
								p("Damage control was");
							elif dmg==6:
								p("Shield control was");
							elif dmg==7:
								p("The library-computer was");
							else:
								p("Nothing was");

							print (" damaged in the attack.~^");
						#}
					 #} //if dmg
				#}	//else
			#}
		#}	//for
		PyTrek.KlingonsMove();
		PyTrek.UpdateStatus();
		PyTrek.ShortRangeScan();
	#}	//end KlingonsShoot

	#//[ KlingonsMove i j k;
	def KlingonsMove(): # {
		i=0; j=0; k=0;
		print("[KlingonsMove]");

		#for (i = 0; i < 64; i++)
		for i in range(0,64):
		#{
			if (PyTrek.trek_sector[i] == PyTrek.KLINGON):
			#{
				j=j+1;                  	#//! Count the number of Klingons in the sector
				PyTrek.trek_sector[i] = 0;  #//! and zero their location
			#}
		#}

		#for (i = 1; i <= j; i++)   //! Position Klingons
		for i in range(1,j):
		#{
			#Retry4: {
			#	k = random_int(64);	// - 1;
			#	if (trek_sector[k] == 0) {
			#		break Retry4;
			#	}
			#}
			#//else
			#//{
			#	trek_sector[k] = KLINGON;
			#//}
			k = random_int(64)
			while (k==0): # {
				k = random_int(64)
			#}
			PyTrek.trek_sector[k] = PyTrek.KLINGON;
		#} end for

		if (PyTrek.trek_klingon_array[0] == 0): # {    //! "Garbage collect" the damage array
			PyTrek.trek_klingon_array[0] = PyTrek.trek_klingon_array[1];
		#}

		if (PyTrek.trek_klingon_array[1] == 0): # {
			PyTrek.trek_klingon_array[1] = PyTrek.trek_klingon_array[2];
		#}
	#}	//end KlingonsMove

	#//[ DamageRepair i j k;
	def DamageRepair(): # {
		i=0; j=0; k=0;
		print("[DamageRepair]");

		if (PyTrek.trek_docked_flag == 1): # //! Docked
		#{
			PyTrek.trek_docked_flag = 2;
			PyTrek.trek_current_energy = PyTrek.MAX_POWER;
			PyTrek.trek_torps_remaining = PyTrek.trek_torp_capacity;
			if (PyTrek.trek_shield_value > 0): # {
				print ("^Shields dropped for docking purposes.^");
			#}

			PyTrek.trek_shield_value = 0;

			j = 0;
			#for (i = 0; i < 8; i++)
			for i in range(0,8):
			#{
				if (PyTrek.trek_damage_array[i] < 5): # {
					j = j + (5 - PyTrek.trek_damage_array[i]);
				#}
			#}

			if (j > 0):
			#{
				print ("^Technicians are standing by to effect repairs to your ship.");
				print ("These repairs will take " + (j / 10) + "." + (j % 10) + " days to ");
				print ("complete. Will you authorize the repair order? (Y/N) ");

				#//c = read_char();	//->k;
				s: str = next_line();
				#//if (c == 'Y' || c == 'y')
				if (s.upper() =="Y"):
				#{
					PyTrek.trek_current_date = PyTrek.trek_current_date + j;
					PyTrek.trek_end_of_time = PyTrek.trek_end_of_time - j;
					if (PyTrek.trek_end_of_time <= 0): # {
						EndOfTime();
					#}
					#for (i = 0; i < 8; i++) {
					for i in range(0,8):
						PyTrek.trek_damage_array[i] = 5;
					#}
					print ("^");
				#}
				else:
				#{
					print (s+". No repairs are being performed^");
				#}
			#}
		#}	//if trek_docked_flag
		else:
		#{
			k = PyTrek.trek_damage_array[PyTrek.DAMAGE_CONTROL];
			#for (i = 0; i < 8; i++)
			for i in range(0,8):
			#{
				if (PyTrek.trek_damage_array[i] < 5 and random_int(20) < k):
				#{
					j = PyTrek.trek_damage_array[i];
					j=j+1;
					PyTrek.trek_damage_array[i] = j;
					print ("^Damage control reports: ~The ");

					#switch(i)
					#{
					#	case 0 : p("warp engines have"); break;
					#	case 1 : p("short range sensors have"); break;
					#	case 2 : p("long range sensors have"); break;
					#	case 3 : p("phaser control system has"); break;
					#	case 4 : p("photon torpedo tubes have"); break;
					#	case 5 : p("damage control system has"); break;
					#	case 6 : p("shield control system has"); break;
					#	case 7 : p("library-computer has"); break;
					#	default:
					#}
					
					if i==0:
						p("warp engines have");
					elif i==1:
						p("short range sensors have");
					elif i==2:
						p("long range sensors have");
					elif i==3:
						p("phaser control system has");
					elif i==4:
						p("photon torpedo tubes have");
					elif i==5:
						p("damage control system has");
					elif i==6:
						p("shield control system has");
					elif i==7:
						p("library-computer has");
					else:
						#default, just make something up
						p("transporters have");
					
					if (j < 5):
						print (" been partially repaired.~^");
					else: # {
						print (" been completely repaired.~^");
					#}
				#} //if trek_damage
			#} //for
		#} //else
	#}	//end DamageRepair


	#//[ PrintQuadrantName x y;
	def QuadrantName(x: int, y: int) -> str:
		galaxy: str = "";
		quadrant: str = "";
		if (x == 1 or x == 2):
		#{
			if (y == 1 or y == 2):
				galaxy = "Antares";
			elif (y == 3 or y ==4):
				galaxy = "Rigel";
			elif (y == 5 or y ==6):
				galaxy = "Procyon";
			elif (y == 7 or y ==8):
				galaxy = "Vega";
			else:
				print("[QuadrantName x = "+str(x)+",y = "+str(y)+"]");	#for debugging
		#}
		elif (x == 3 or x== 4):
		#{
			if (y == 1 or y ==2):
				galaxy = "Canopus";
			elif (y == 3 or y ==4):
				galaxy = "Altair";
			elif (y == 5 or y ==6):
				galaxy = "Sagittarius";
			elif (y == 7 or y ==8):
				galaxy = "Pollux";
			else:
				print("[QuadrantName x = "+str(x)+",y = "+str(y)+"]");	#for debugging
		#}
		elif (x == 5 or x==6):
		#{
			if (y == 1 or y == 2):
				galaxy = "Sirius";
			elif (y == 3 or y ==4):
				galaxy = "Deneb";
			elif (y == 5 or y ==6):
				galaxy = "Capella";
			elif (y == 7 or y ==8):
				galaxy = "Betelgeuse";
			else:
				print("[QuadrantName x = "+str(x)+",y = "+str(y)+"]");	#for debugging
		#}
		elif (x == 7 or x==8):
		#{
			if (y == 1 or y ==2):
				galaxy = "Aldebaran";
			elif (y == 3 or y ==4):
				galaxy = "Regulus";
			elif (y == 5 or y ==6):
				galaxy = "Arcturus";
			elif (y == 7 or y ==8):
				galaxy = "Spica";
			else:
				print("[QuadrantName x = "+str(x)+",y = "+str(y)+"]");	#for debugging
		#}
		else:
			print("[QuadrantName x = "+str(x)+",y = "+str(y)+"]");	#for debugging

		#//if (x == 1 or 3 or 5 or 7)
		if ( (x % 2) == 1):
		#{
			#//if (y == 1 or 3 or 5 or 7)
			if ( (y % 2) == 1):
				quadrant = " I";
			else:
				quadrant = " III";
		#}

		#//if (x == 2 or 4 or 6 or 8)
		if ( (x % 2) == 0):
		#{
			#//if (y == 1 or 3 or 5 or 7)
			if ( (y % 2) == 1):
				quadrant = " II";
			else:
				quadrant = " IV";
		#}
		return galaxy + quadrant;
	#}

	# I don't understand what this is doing.
	# Renamed RangeTrek from Range so it doesn't conflict with range
	#//[ Range x1 y1 x2 y2 delta_x delta_y result;
	#public static int Range(int x1, int y1,int x2,int y2) {
	def RangeTrek(x1: int, y1: int, x2: int, y2: int) -> int:
		delta_x=0; delta_y=0; result=0;
		delta_x = (x1 - x2) * 10;
		delta_x = delta_x * delta_x;

		delta_y = (y1 - y2) * 10;
		delta_y = delta_y * delta_y;

		result = PyTrek.SquareRoot(delta_x + delta_y);
		return result;
	#}


	#//! Brute force approach to finding the square root of a number
	#//[ SquareRoot a b;
	#public static int SquareRoot(int a) {
	def SquareRoot(a: int) -> int:
		return int(math.sqrt(a))
		#//for (b = 1: b <= 110: b++)
		#//{
		#//if (b * b > a)
		#// return (b - 1);
		#//}
		#return (int)Math.sqrt(a);	
	#}

	#//[ ShipDestroyed ;
	def ShipDestroyed(): # {
		print("The Enterprise has been destroyed. You have failed. ");
		PyTrek.LoseGame();
	#}

	#//[ OutOfEnergy ;
	def OutOfEnergy(): # {
		print("^You've stranded yourself in space without enough energy to get to a base! ");
		PyTrek.LoseGame();
	#}

	#//[ EndOfTime ;
	def EndOfTime(): # {
		print ("You've run out of time, Captain! ");
		PyTrek.LoseGame();
	#}

	#//[ LoseGame ;
	def LoseGame(): # {
		print ("It is stardate " + str(PyTrek.trek_current_date // 10) + "." +str(PyTrek.trek_current_date % 10) + ". ");

		#//print "There ";
		p("There ");

		if (PyTrek.trek_klingons_left == 1): # {
			#//print "was ";
			p("was ");
		#}
		else:
		#{
			#//print "were ";
			p("were ");
		#}
		p( str(PyTrek.trek_klingons_left)+ " Klingon battlecruiser");

		if (PyTrek.trek_klingons_left == 1):
			p("s");

		print (" left at the end of your mission.^^");

		#//print "[Press any key to continue.]^";
		PyTrek.Pause();
		PyTrek.EndScreen();
	#}

	#//[ WonGame ;
	def WonGame(): # {
		print ("Congratulations, Captain! You have destroyed the last Klingon battlecruiser in your patrol area.^^");
		print ("Starfleet awards you the Medal of Valor");
		PyTrek.UnitedFederation();
		#//print "[Press any key to continue.]^";
		PyTrek.Pause();
		PyTrek.EndScreen();
	#}

	#//[ EndScreen ;
	def EndScreen(): # {
		#//@set_cursor 1 1;
		#//@split_window 0;
		#//@erase_window $ffff;

		print ("^Thanks for playing Super Z Trek.^^");
		#//@quit;
		#System.exit(0);
		exit();
	#}

	#//[ Pause dummy;
	#//@read_char 1 dummy;
	#//return dummy;
	#//];

	#//[ Help i;
	def Help(): # {
		print("[Help]");
		print("^Choose which file to read:^^");
		print("1: How To Play Super Z Trek^");
		print("2: About This Game^");
		print("3: Exit^^");
		print("Enter choice: ");

		i: int = read_int();
		while (i<0): # {
			i = read_int();
		#}
   		#//@read_char 1 -> i;
   		#//print i - 48, "^";
   		#switch(i)
   		#{
   		#   case 1 : HowToPlay(); break;
   		#   case 2 : About(); break;
   		#   case 3 : print("^Library-computer exited.^^"); break;
   		#   default: print("^Invalid choice.^ '"+(int)i+"'");
   		#}
		if (i==1):
			PyTrek.HowToPlay();
		elif i==2:
			PyTrek.About();
		elif i==3:
			print("^Library-computer exited.^^");
		else:
			print("^Invalid choice.^ '"+i+"'");
		return;
	#} end help

	#//[ HowToPlay ;
	def HowToPlay(): # {
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
		PyTrek.PrintCompass();
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
		return;
	#}

	#//[ About ;
	def About():	# {
		print("This is a Python version of a Java version of Star Trek, that was based on");
		print("an Inform version dated 2/28/2000 found at:");
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
		Pause();
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
		print("AS SEEN ON THE STAR TREK TV SHOW CREATED BY GENE RODDENBERRY.^");
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
		return;
	#}

	def Enterprise(): # {
		#//from https://www.asciiart.eu/television/star-trek
		print("     ___________________________            ____");
		print("...  \\____NCC_1701A_________|_// __=*=__.--'----'--._________");
		print("                    \\  |        /-------.__________.--------'");
		print("               /=====\\ |======/      '     '----'");
		print("                  \\________          }]");
		print("                           `--------'		");
	#}

	def Enterprise2(): #{
		print("___________________          _-_");
		print("\\==============_=_/ ____.---'---`---.____");
		print("            \\_ \\    \\----._________.----/");
		print("              \\ \\   /  /    `-_-'");
		print("          __,--`.`-'..'-_");
		print("         /____          ||");
		print("              `--.____,-'	");
	#}

	def UnitedFederation(): # {
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
	#}

	def KlingonBirdOfPrey(): # {
		print("                        _------_        _------_");
		print("                       / /~~~~~~~\\----/~~~~~~~\\ \\");
		print("                    __|_|    /~ _-~~~~-_ ~\\    |_|__");
		print("              __--~~____|   |  /________\\  |   |____~~--__");
		print("        __--~~__--~~     ~---__\\   ()   /__---~     ~~--__~~--__");
		print("     /~~__--~~                  ~--__--~                  ~~--__~~\\");
		print("   / /~~                                                        ~~\\ \\");
		print(" / /                                                                \\ \\");
		print("(0)                                                                  (0)");
		#}
#} end class PyTrek
#--------------------------------------

#//utility functions
	
#//return a random number from 0..(i-1)
#public static int random(int i) {
#	return (int)(Math.floor(Math.random()*i));
#}
def random_int(i: int) -> int:
	return random.randint(0, i);

def Pause():
	input("(Press Enter to continue...)")

def new_line():
	print()

def read_int() -> int:
	value = input()
	while(value==None):
		value=input("?");
	try:
		return int(value);
	except ValueError:
		print("[read_int: unable to parse "+value+" to int]")
		return -1
				
def type_as_string(value: Any) -> str:
	return type(value).__name__
		
def next_line() -> str:
	return input()
	
#public static void p(String s) {System.out.print(s);}
#public static void p(int i) {System.out.print(i);}
#write without newline
def p(v: Any):
	if type(v) == str:
		sys.stdout.write(v);
	else:
		sys.stdout.write( str(v));
#end def

#program runner
if __name__ == '__main__':
	PyTrek.main()
