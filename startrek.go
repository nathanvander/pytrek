package main

import (
    "fmt"
    //"math"
    "math/rand"
    //"unicode"
    "time"
    "bufio"
    "os"
    "log"
    "strings"
)

func main() {
	PlayTrek()
}

/*
 * Modified from https://raw.githubusercontent.com/EtchedPixels/FUZIX/master/Applications/games/startrek.c
 * I like this version better than the original c code because it doesn't use floating point
 * and it has better variable names
 *
 * startrek.c
 *
 * Super Star Trek Classic (v1.1)
 * Retro Star Trek Game 
 * C Port Copyright (C) 1996  <Chris Nystrom>
 *
 * Reworked for Fuzix by Alan Cox (C) 2018
 *	- Removed all floating point
 *	- Fixed multiple bugs in the BASIC to C conversion
 *	- Fixed a couple of bugs in the BASIC that either got in during it's
 *	  conversion between BASICs or from the original trek
 *	- Put it on a diet to get it to run in 32K. No features were harmed
 *	  in the making of this code smaller.
 *
 * TODO:
 *	- Look hard at all the rounding cases
 *	- Review some of the funnies in the BASIC code that appear to be bugs
 *	  either in the conversion or between the original and 'super' trek
 *	  Notably need to fix the use of shield energy directly for warp
 *	- Find a crazy person to draw ascii art bits we can showfile for things
 *	  like messages from crew/docking/klingons etc
 *	- I think it would make a lot of sense to switch to real angles, but
 *	  trek game traditionalists might consider that heresy.
 *
 * 
 * This program is free software; you can redistribute it and/or modify
 * in any way that you wish. _Star Trek_ is a trademark of Paramount
 * I think.
 * 
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 *
 * This is a C port of an old BASIC program: the classic Super Star Trek
 * game. It comes from the book _BASIC Computer Games_ edited by David Ahl
 * of Creative Computing fame. It was published in 1978 by Workman Publishing,
 * 1 West 39 Street, New York, New York, and the ISBN is: 0-89489-052-3.
 * 
 * See http://www.cactus.org/~nystrom/startrek.html for more info.
 *
 * Contact Author of C port at:
 *
 * Chris Nystrom
 * 1013 Prairie Dove Circle
 * Austin, Texas  78758
 *
 * E-Mail: cnystrom@gmail.com, nystrom@cactus.org
 *
 * BASIC -> Conversion Issues
 *
 *     - String Names changed from A$ to sA
 *     - Arrays changed from G(8,8) to map[9][9] so indexes can
 *       stay the same.
 *
 * Here is the original BASIC header:
 *
 * SUPER STARTREK - MAY 16, 1978 - REQUIRES 24K MEMORY
 *
 ***        **** STAR TREK ****        ****
 *** SIMULATION OF A MISSION OF THE STARSHIP ENTERPRISE,
 *** AS SEEN ON THE STAR TREK TV SHOW.
 *** ORIGINAL PROGRAM BY MIKE MAYFIELD, MODIFIED VERSION
 *** PUBLISHED IN DEC'S "101 BASIC GAMES", BY DAVE AHL.
 *** MODIFICATIONS TO THE LATTER (PLUS DEBUGGING) BY BOB
 *** LEEDOM - APRIL & DECEMBER 1974,
 *** WITH A LITTLE HELP FROM HIS FRIENDS . . .
 *** COMMENTS, EPITHETS, AND SUGGESTIONS SOLICITED --
 *** SEND TO:  R. C. LEEDOM
 ***           WESTINGHOUSE DEFENSE & ELECTRONICS SYSTEMS CNTR.
 ***           BOX 746, M.S. 338
 ***           BALTIMORE, MD  21203
 ***
 *** CONVERTED TO MICROSOFT 8 K BASIC 3/16/78 BY JOHN BORDERS
 *** LINE NUMBERS FROM VERSION STREK7 OF 1/12/75 PRESERVED AS
 *** MUCH AS POSSIBLE WHILE USING MULTIPLE STATMENTS PER LINE
 *
 */

/**
* Further notes:
* I was trying to just convert this to Go without refactoring, but this will
* need a few modifications, just to compile
*	1. All numbers use uint16.  This is because Go is very picky and it is a pain to convert from 
*	   a type to another.  An exception is in the c[] array (which has something to do with 
*		course control) and which uses -1.  Also the damage array can hold values less than 0  
*	2. Some functions return a -1 to indicate an error or not found.  This should return 65535
*	3. All arrays are 1 based.  Since Go arrays are 0-based, make them 1 bigger and leave the 
*		0th element blank.
*	4. Stardates have 5 digits starting with a 1..5.  The last digit is the fraction.
*		For example 41234 means 4123.4
*	5. Course is a number from 0..900.  900 means the same as 100.  I don't know what a course of less
*		than 100 means, but I will leave that.
*	6. Warp speed is a number from 0..800.
*	7. Coordinates are also from 0..900
*
*  This code is crying out for refactoring but I am trying to not make any other changes now.
*/

//#include <stdio.h>
//#include <stdlib.h>
//#include <string.h>
//#include <stdint.h>
//#include <time.h>
//#include <unistd.h>
//#include <ctype.h>

//#ifndef TREK_DIR
//#define TREK_DIR	"/usr/lib/trek/"
//#endif

/* Standard Terminal Sizes */

const MAXROW = 24
const MAXCOL = 80

type klingon struct {
	y uint16;
	x uint16;
	energy uint16;
};

/* Function Declarations */
//static void intro(void);
//static void new_game(void);
//static void initialize(void);
//static void new_quadrant(void);
//static void course_control(void);
//static void complete_maneuver(uint16_t, uint16_t);
//static void maneuver_energy(uint16_t);
//static void short_range_scan(void);
//static void long_range_scan(void);
//static void phaser_control(void);
//static void photon_torpedoes(void);
//static void torpedo_hit(uint8_t y, uint8_t x);
//static void damage_control(void);
//static void shield_control(void);
//static void library_computer(void);
//static void galactic_record(void);
//static void status_report(void);
//static void torpedo_data(void);
//static void nav_data(void);
//static void dirdist_calc(void);
//static void galaxy_map(void);
//static void end_of_time(void);
//static void resign_commision(void);
//static void won_game(void);
//static void end_of_game(void);
//static void klingons_move(void);
//static void klingons_shoot(void);
//static void repair_damage(uint16_t warp);
//static void find_set_empty_place(uint8_t t, uint8_t *z1, uint8_t *z2);
//static const char *get_device_name(int n);
//static void quadrant_name(uint8_t small, uint8_t y, uint8_t x);
//static int distance_to(struct klingon *k);
//static int square00(int16_t t);
//static int cint100(int16_t d);
//static void compute_vector(int16_t, int16_t, int16_t, int16_t);
//static void showfile(char *filename);

/* Global Variables */
var starbases uint16;					/* Starbases in Quadrant */
var base_y, base_x uint16;			/* Starbase Location in sector */
var starbases_left uint16;			/* Total Starbases */

//static int8_t c[3][10] =	/* Movement indices 1-9 (9 is wrap of 1) */
// c means course
var c = [3][10]int16 {			//note different type
	{0, 0, 0,  0,  0,  0, 0, 0, 0, 0},
	{0, 0, -1, -1, -1, 0, 1, 1, 1, 0},
	{1, 1, 1,  0,  -1,-1,-1, 0, 1, 1}}

var docked uint16;					/* Docked flag */
var energy uint16;					/* Current Energy */
const energy0 uint16 = 3000;			/* Starting Energy */
var gmap [9][9]uint16;		/* Galaxy. BCD of k b s plus flag */
const MAP_VISITED uint16 = 0x1000		/* Set if this sector was mapped */
var kdata [4]*klingon				/* Klingon Data */
var klingons uint16;				/* Klingons in Quadrant */
var total_klingons uint16;			/* Klingons at start */
var klingons_left uint16;			/* Total Klingons left */
var torps uint16;				/* Photon Torpedoes left */
const torps0 = 10;				/* Photon Torpedo capacity */
var quad_y, quad_x uint16;		/* Quadrant Position of Enterprise */
var shield uint16;			/* Current shield value */
var stars uint16;			/* Stars in quadrant */
var time_start uint16;			/* Starting Stardate */
var time_up uint16;			/* End of time */
var damage [9]int16;			/* Damage Array */
var d4 uint16;				/* Used for computing damage repair time */
var ship_y, ship_x uint16;		/* Current Sector Position of Enterprise, fixed point */
var stardate uint16;			/* Current Stardate */
var quad [8][8]uint16;
const Q_SPACE =		0
const Q_STAR =		1
const Q_BASE =		2
const Q_KLINGON =	3
const Q_SHIP =		4

//static char quadname[12];		/* Quadrant name */
var quadname string				/* Quadrant name */

//used in short range scan
var tilestr = [5]string {"   "," * ",">!<","+K+","<*>"};

var device_name = [9]string{"", "Warp engines", "Short range sensors", "Long range sensors",
	"Phaser control", "Photon tubes", "Damage control", "Shield control","Library computer"};

/* We probably need double digit for co-ordinate maths, single for time */
//#define TO_FIXED(x)	((x) * 10)
func TO_FIXED(x uint16) uint16 { return x*10}
//#define FROM_FIXED(x)	((x) / 10)
func FROM_FIXED(x uint16) uint16 { return x / 10}

//#define TO_FIXED00(x)	((x) * 100)
//#define FROM_FIXED00(x)	((x) / 100)
func TO_FIXED00(x uint16) uint16 { return x*100}
func FROM_FIXED00(x uint16) uint16 { return x / 100}

//-----------------------
/*
 *	Returns an integer from 1 to spread
 */
func get_rand(spread uint16) uint16 {
	return uint16(rand.Intn( int(spread) ) + 1);
	//uint16_t r = rand();
	/* RAND_MAX is at least 15 bits, our largest request is for 500. The
	   classic unix rand() is very poor on the low bits so swap the ends
	   over */
	//r = (r >> 8) | (r << 8);
	//return ((r % spread) + 1);
}

/*
 *	Get a random co-ordinate
 */
func rand8() uint16 {
	return get_rand(8);
}

/* This is basically a fancier fgets that always eats the line even if it
   only copies part of it */
//static void input(char *b, uint8_t l)
//{
//	int c;
//
//	fflush(stdout);
//	while((c = getchar()) != '\n') {
//		if (c == EOF)
//			exit(1);
//		if (l > 1) {
//			*b++ = c;
//			l--;
//		}
//	}
//	*b = 0;
//}
func get_input() string {
	var inp string
	fmt.Scanln(&inp)
	return inp
}

//static uint8_t yesno(void)
//{
//	char b[2];
//	input(b,2);
//	if (tolower(*b) == 'y')
//		return 1;
//	return 0;
//}
func yesno() bool {
	var inp string
	var firstchar string
	
	inp = get_input()
	firstchar = inp[0:1]
	firstchar = strings.ToLower(firstchar)

	if firstchar == "y" {
		return true
	} else {
		return false
	}
}

/* Input a value between 0.00 and 9.99 */
//static int16_t input_f00(void)
//{
//	int16_t v;
//	char buf[8];
//	char *x;
//	input(buf, 8);
//	x = buf;
//	if (!isdigit(*x))
//		return -1;
//	v = 100 * (*x++ - '0');
//	if (*x == 0)
//		return v;
//	if (*x++ != '.')
//		return -1;
//	if (!isdigit(*x))
//		return -1;
//	v += 10 * (*x++ - '0');
//	if (!*x)
//		return v;
//	if (!isdigit(*x))
//		return -1;
//	v += *x++ - '0';
//	return v;
//}

/** Input a value between 0.00 and 9.99 
* We just accept the floating point input, multiply by 100
* and convert to an int, so this should be from 0..999
* but we don't check the range here.
* Returns -1 for input error
*/
func input_f00() uint16 {
	var f float32
	_, err := fmt.Scanf("%f", &f)
	if err != nil {
		fmt.Println(err)
		return 65535;	//-1
	} else {
		return uint16(f*100)
	}
}

/* Integer: unsigned, or returns -1 for blank/error */
//static int input_int(void)
//{
//	char x[8];
//	input(x, 8);
//	if (!isdigit(*x))
//		return -1;
//	return atoi(x);
//}
func input_int() uint16 {
	var i uint16
	_, err := fmt.Scan(&i)
	if err != nil {
		fmt.Println(err)
		return 65535
	} else {
		return i
	}
}

//static const char *print100(int16_t v)
//{
//	static char buf[16];
//	char *p = buf;
//	if (v < 0) {
//		v = -v;
//		*p++ = '-';
//	}
//	p += sprintf(p, "%d.%02d", v / 100, v%100);
//	return buf;
//}

/**
* convert an int as if it were a float with 2 digits
*/
func print100(v uint16) string {
	return fmt.Sprintf("%d.%02d", v / 100, v%100);
}

//int main(int argc, char *argv[])
//{
//	chdir(TREK_DIR);
//	intro();
//	new_game();
//	return (0);
//}
/* Main Program 
* Call this from the main package
*/
func PlayTrek() {
	intro()
	new_game()
}

//static uint8_t inoperable(uint8_t u)
//{
//	if (damage[u] < 0) {
//		printf("%s %s inoperable.\n",
//			get_device_name(u),
//			u == 5 ? "are":"is");
//		return 1;
//	}
//	return 0;
//}
func inoperable(u uint16) bool {
	if damage[u] < 0 {
		fmt.Printf("%s is inoperable.\n", get_device_name(u) )
		return true
	} else {
		return false
	}
}

//static void intro(void)
//{
//	showfile("startrek.intro");
//	if (yesno())
//		showfile("startrek.doc");
//	showfile("startrek.logo");
//
//	/* Seed the randomizer with the timer */
//	srand((unsigned) time(NULL));
//
//	/* Max of 4000, which works nicely with our 0.1 fixed point giving
//	   us a 16bit unsigned range of time */
//	stardate = TO_FIXED((get_rand(20) + 20) * 100);
//}

func intro() {
	TrekIntro()
	fmt.Print("Do you need instructions (y/n):")
	
	if (yesno()) {
		showfile("startrek.txt");
	}
	//seed the randomizer
	rand.Seed(time.Now().UnixNano())
	stardate = TO_FIXED((get_rand(20) + 20) * 100);
}

func TrekIntro() {
   		fmt.Println("************************************");
       	fmt.Println("*                                  *");
       	fmt.Println("*                                  *");
       	fmt.Println("*       * * Super Go Trek * *       *");
       	fmt.Println("*                                  *");
       	fmt.Println("*                                  *");
       	fmt.Println("************************************");
   		fmt.Println("^^^");
   		//spaces (0->33)/2 - 12;
   		Enterprise();

   		Pause();
	}

func Enterprise() {
		//from https://www.asciiart.eu/television/star-trek
fmt.Println("     ___________________________            ____");
fmt.Println("...  \\____NCC_1701A_________|_// __=*=__.--'----'--._________");
fmt.Println("                    \\  |        /-------.__________.--------'");
fmt.Println("               /=====\\ |======/      '     '----'");
fmt.Println("                  \\________          }]");
fmt.Println("                           `--------'		");
}

func Pause() {
	fmt.Println("(Press Enter to continue)");
    var line string
    fmt.Scanf("%s", &line)
}

func Fatal() {
	fmt.Println("** Fatal Error **   You've just stranded your ship in space.")
	fmt.Println("")
	fmt.Println("You have insufficient maneuvering energy, and Shield Control is presently")
	fmt.Println("incapable of cross circuiting to engine room!!")
}

func new_game() {
	initialize();
	new_quadrant();
	short_range_scan();
	MainMenu()
}

func MainMenu() {
	var cmd string
	for {
		if (shield + energy <= 10 && (energy < 10 || damage[7] < 0)) {
			//showfile("startrek.fatal");
			Fatal()
			end_of_time();
		}

		fmt.Print("Command? ");
		cmd = get_input();

		// switch?
		if (cmd == "nav") {
			course_control()
		} else if (cmd ==  "srs") {
			short_range_scan()
		} else if (cmd == "lrs") {
			long_range_scan()
		} else if (cmd == "pha") {
			phaser_control()
		} else if (cmd == "tor") {
			photon_torpedoes()
		} else if (cmd == "shi") {
			shield_control()
		} else if (cmd == "dam") {
			damage_control()
		} else if (cmd == "com") {
			library_computer()
		} else if (cmd == "xxx") {
			resign_commision()
		} else {
			fmt.Println("Enter one of the following:");
			fmt.Println("  nav - To Set Course");
			fmt.Println("  srs - Short Range Sensors");
			fmt.Println("  lrs - Long Range Sensors");
			fmt.Println("  pha - Phasers");
			fmt.Println("  tor - Photon Torpedoes");
			fmt.Println("  shi - Shield Control");
			fmt.Println("  dam - Damage Control");
			fmt.Println("  com - Library Computer");
			fmt.Println("  xxx - Resign Command");
		}
	}
}


//static void initialize(void)
func initialize() {
	var i, j uint16;
	var yp, xp uint16;

	/* Initialize time */
	time_start = FROM_FIXED(stardate);
	time_up = 25 + get_rand(10);

	/* Initialize Enterprise */
	docked = 0;
	energy = energy0;
	torps = torps0;
	shield = 0;

	quad_y = rand8();
	quad_x = rand8();
	ship_y = TO_FIXED00( rand8());		
	ship_x = TO_FIXED00( rand8());

	for i = 1; i <= 8; i++ {
		damage[i] = 0;
	}

	/* Setup What Exists in Galaxy */
	for i = 1; i <= 8; i++ {
		for j = 1; j <= 8; j++ {
			r := get_rand(100);
			klingons = 0;
			if r > 98 {
				klingons = 3;
			} else if r > 95 {
				klingons = 2;
			} else if r > 80 {
				klingons = 1;
			}

			klingons_left = klingons_left + klingons;
			starbases = 0;

			if get_rand(100) > 96 {
				starbases = 1;
			}

			starbases_left = starbases_left + starbases;

			gmap[i][j] = uint16( (klingons << 8) + (starbases << 4) + rand8() );
		}
	}

	/* Give more time for more Klingons */
	if klingons_left > time_up {
		time_up = klingons_left + 1;
	}

	/* Add a base if we don't have one */
	if starbases_left == 0 {
		yp = rand8();
		xp = rand8();
		if (gmap[yp][xp] < 0x200) {
			gmap[yp][xp] += (1 << 8);
			klingons_left++;
		}

		gmap[yp][xp] += (1 << 4);
		starbases_left++;
	}

	total_klingons = klingons_left;

	MissionBrief()
}

func MissionBrief() {
	fmt.Println("Your orders are as follows:")
	fmt.Printf(" Destroy the %d Klingon warships which have invaded\n", klingons_left)
	fmt.Println(" the galaxy before they can attack Federation Headquarters")
	fmt.Printf(" on stardate %u. This gives you %d days.\n", time_start + time_up, time_up)
	fmt.Printf("There are %d starbases in the galaxy for resupplying your ship.\n\n",starbases_left)
	fmt.Println("Hit any key to accept command. ")
	get_input()
}

func place_ship() {
	quad[FROM_FIXED00( ship_y - 1)][FROM_FIXED00( ship_x - 1)] = Q_SHIP;
}

func new_quadrant() {
	var i uint16;
	var tmp uint16;
	//struct klingon *k = kdata;
	var k *klingon		//k is a pointer to a klingon struct

	klingons = 0;
	starbases = 0;
	stars = 0;

	/* Random factor for damage repair. We compute it on each new
	   quadrant to stop the user just retrying until they get a number
	   they like. The conversion here was wrong and now copies the BASIC
	   code generate 0.00 to 0.49 */
	d4 =  get_rand(50) - 1;

	/* Copy to computer */
	gmap[quad_y][quad_x] |= MAP_VISITED;

	if (quad_y >= 1 && quad_y <= 8 && quad_x >= 1 && quad_x <= 8) {
		quadname = quadrant_name(0, quad_y, quad_x);

		if (TO_FIXED(time_start) != stardate) {
			fmt.Printf("Now entering %s quadrant...\n\n", quadname);
		} else {
			fmt.Println("\nYour mission begins with your starship located");
			fmt.Printf("in the galactic quadrant %s.\n\n", quadname);
		}
	}

	tmp = gmap[quad_y][quad_x];
	klingons = (tmp >> 8) & 0x0F;
	starbases = (tmp >> 4) & 0x0F;
	stars = tmp & 0x0F;

	if (klingons > 0) {
		fmt.Println("Combat Area  Condition Red");

		if (shield < 200) {
			fmt.Println("Shields Dangerously Low");
		}
	}

	//initialize klingons
	for i = 0; i < 3; i++ {
		k = new(klingon)
		k.y = 0;
		k.x = 0;
		k.energy = 0;
		kdata[i] = k;
	}

	//memset(quad, Q_SPACE, 64);

	place_ship();
	
	if (klingons > 0) {
		for i = 0; i < klingons; i++ {
			k = kdata[i]
			k.y,k.x = find_set_empty_place(Q_KLINGON);
			k.energy = 100 + get_rand(200);
		}
	}

	if starbases > 0  {
		base_y,base_x = find_set_empty_place(Q_BASE);
	}

	for i = 1; i <= stars; i++ {
		find_set_empty_place(Q_STAR);
	}
}

func course_control() {
	var i uint16;
	var c1 uint16;
	var warp uint16;
	var n uint16; 
	var c2, c3, c4 uint16;
	var z1, z2 uint16;
	var x1, x2 int16;	//note int16
	var x, y uint16;
	//static char warpmax[4] = "8";
	var warpmax string = "8"

	fmt.Println("Course (0-9): ");

	c1 = input_f00();

	if c1 == 900 {
		c1 = 100;
	}

	if (c1 < 0 || c1 > 900) {
		fmt.Println("Lt. Sulu reports:\n  Incorrect course data, sir!\n");
		return;
	}

	if (damage[1] < 0) {
		//strcpy(warpmax, "0.2");
		warpmax = "0.2"
	}

	fmt.Printf("Warp Factor (0-%s): ", warpmax);

	warp = input_f00();

	if (damage[1] < 0 && warp > 20) {
		fmt.Printf("Warp Engines are damaged. Maximum speed = Warp 0.2.\n\n");
		return;
	}

	if (warp <= 0) {
		return;
	}

	if (warp > 800) {
		fmt.Println("Chief Engineer Scott reports:")
		fmt.Printf("  The engines won't take warp %s!\n\n", print100(warp));
		return;
	}

	n = warp * 8;

	n = cint100(n);	

	/* FIXME: should be  s + e - n > 0 iff shield control undamaged */
	if (energy - n < 0) {
		fmt.Println("Engineering reports:")
		fmt.Println("  Insufficient energy available for maneuvering")
		fmt.Printf(" at warp %s!\n\n", print100(warp));

		if (shield >= n && damage[7] >= 0) {
			fmt.Println("Deflector Control Room acknowledges:")
			fmt.Printf("  %d units of energy presently deployed to shields.\n", shield);
		}
		return;
	}

	klingons_move();

	repair_damage(warp);

	z1 = FROM_FIXED00(ship_y);
	z2 = FROM_FIXED00(ship_x);
	quad[z1-1][z2-1] = Q_SPACE;


	c2 = FROM_FIXED00(c1);	/* Integer part */
	c3 = c2 + 1;		/* Next integer part */
	c4 = (c1 - TO_FIXED00(c2));	/* Fractional element in fixed point */

	x1 = 100 * c[1][c2] + (c[1][c3] - c[1][c2]) * int16(c4);
	x2 = 100 * c[2][c2] + (c[2][c3] - c[2][c2]) * int16(c4);

	x = ship_y;
	y = ship_x;

	for i = 1; i <= n; i++ {
//		printf(">%d %d %d %d %d\n",
//			i, ship_y, ship_x, x1, x2);
		//x1 and x2 can theoretically be negative here
		ship_y = uint16( int16(ship_y) + x1);
		ship_x = uint16( int16(ship_x) + x2);

//		printf("=%d %d %d %d %d\n",
//			i, ship_y, ship_x, x1, x2);

		z1 = FROM_FIXED00(ship_y);
		z2 = FROM_FIXED00(ship_x);	/* ?? cint100 ?? */

		/* Changed quadrant */
		if (z1 < 1 || z1 >= 9 || z2 < 1 || z2 >= 9) {
			outside := 0;		/* Outside galaxy flag */
			quad_y_old := quad_y;
			quad_x_old := quad_x;

			//x1 and x2 can theoretically be negative here
			x = (800 * quad_y) + uint16(int16(x) + (int16(n) * x1));
			y = (800 * quad_x) + uint16(int16(y) + (int16(n) * x2));

			//	printf("X %d Y %d\n", x, y);

			quad_y = x / 800;	/* Fixed point to int and divide by 8 */
			quad_x = y / 800;	/* Ditto */

			//	printf("Q %d %d\n", quad_y, quad_x);

			ship_y = x - (quad_y * 800);
			ship_x = y - (quad_x * 800);

			//	printf("S %d %d\n", ship_y, ship_x);

			if (ship_y < 100) {
				quad_y = quad_y - 1;
				ship_y = ship_y + 800;
			}

			if (ship_x < 100) {
				quad_x = quad_x - 1;
				ship_x = ship_x + 800;
			}

			/* check if outside galaxy */

			if (quad_y < 1) {
				outside = 1;
				quad_y = 1;
				ship_y = 100;
			}

			if (quad_y > 8) {
				outside = 1;
				quad_y = 8;
				ship_y = 800;
			}

			if (quad_x < 1) {
				outside = 1;
				quad_x = 1;
				ship_x = 100;
			}

			if (quad_x > 8) {
				outside = 1;
				quad_x = 8;
				ship_x = 800;
			}

			if (outside == 1) {
				/* Mostly showfile ? FIXME */
				fmt.Println("LT. Uhura reports:\n")
		       	fmt.Println("  Message from Starfleet Command:\n\n")
		       	fmt.Println("  Permission to attempt crossing of galactic perimeter\n")
		       	fmt.Println("  is hereby *denied*. Shut down your engines.\n\n")
		       	fmt.Println("Chief Engineer Scott reports:\n")
		       	fmt.Printf("  Warp Engines shut down at sector %d, %d", FROM_FIXED00(ship_y),FROM_FIXED00(ship_x)) 
		       	fmt.Printf("  of quadrant %d, %d.\n\n",quad_y, quad_x);
			}
			maneuver_energy(n);

			/* this section has a different order in the original.
			   t = t + 1;

			   if (t > time_start + time_up)
			   end_of_time();
			 */

			if (FROM_FIXED(stardate) > time_start + time_up) {
				end_of_time();
			}

			if (quad_y != quad_y_old || quad_x != quad_x_old) {
				stardate = stardate + TO_FIXED(1);
				new_quadrant();
			}
			complete_maneuver(warp, n);
			return;
		}

		if (quad[z1-1][z2-1] != Q_SPACE) {	/* Sector not empty */
			//x1 and x2 can theoretically be negative
			ship_y = uint16(int16(ship_y) - x1);
			ship_x = uint16(int16(ship_x) - x2);
			fmt.Println("Warp Engines shut down at sector ")
			fmt.Printf("%d, %d due to bad navigation.\n\n", z1, z2);
			i = n + 1;
		}
	}
	complete_maneuver(warp, n);
}

func complete_maneuver(warp uint16, n uint16) {
	var time_used uint16;

	place_ship();
	maneuver_energy(n);

	time_used = TO_FIXED(1);

	/* Ick FIXME - re really want to tidy up time to FIXED00 */
	if (warp < 100) {
		time_used = TO_FIXED(FROM_FIXED00(warp));
	}

	stardate += time_used;

	if (FROM_FIXED(stardate) > time_start + time_up) {
		end_of_time();
	}

	short_range_scan();
}


func maneuver_energy(n uint16) {
	energy -= n + 10;

	if (energy >= 0) {
		return;
	}

	/* FIXME:
	   This never occurs with the nav code as is - ancient trek versions
	   included shield power in movement allowance if shield control
	   was undamaged */
	fmt.Println("Shield Control supplies energy to complete maneuver.\n");

	shield = shield + energy;
	energy = 0;

	if (shield <= 0) {
		shield = 0;
	}
}

const srs_1 string = "------------------------"

func short_range_scan() {
	
	var i, j uint16;
	//char *sC = "GREEN";
	var condition string = "GREEN";
	var y1, y2 uint16
	var x1, x2 uint16

	if (energy < energy0 / 10) {
		condition = "YELLOW";
	}

	if (klingons > 0) {
		condition = "*RED*";
	}

	docked = 0;

	y1 = FROM_FIXED00(ship_y) - 1
	y2 = FROM_FIXED00(ship_y) + 1
	x1 = FROM_FIXED00(ship_x) - 1
	x2 = FROM_FIXED00(ship_x) + 1
	for i = y1; i <= y2 ; i++ {
		for j = x1; j <= x2; j++ {
			if (i >= 1 && i <= 8 && j >= 1 && j <= 8) {
				if (quad[i-1][j-1] == Q_BASE) {
					docked = 1;
					condition = "DOCKED";
					energy = energy0;
					torps = torps0;
					fmt.Println("Shields dropped for docking purposes.");
					shield = 0;
				}
			}
		}
	}

	if (damage[2] < 0) {
		fmt.Println("\n*** Short Range Sensors are out ***");
		return;
	}

	fmt.Println(srs_1);
	for i = 0; i < 8; i++ {
		for j = 0; j < 8; j++ {
			fmt.Println(tilestr[quad[i][j]]);
		}

		switch i {
			case 0:
				fmt.Printf("    Stardate            %d\n", FROM_FIXED(stardate));
			case 1:
				fmt.Printf("    Condition           %s\n", condition);
			case 2:
				fmt.Printf("    Quadrant            %d, %d\n", quad_y, quad_x);
			case 3:
				fmt.Printf("    Sector              %d, %d\n", FROM_FIXED00(ship_y), FROM_FIXED00(ship_x));
			case 4:
				fmt.Printf("    Photon Torpedoes    %d\n", torps);
			case 5:
				fmt.Printf("    Total Energy        %d\n", energy + shield);
			case 6:
				fmt.Printf("    Shields             %d\n", shield);
			case 7:
				fmt.Printf("    Klingons Remaining  %d\n", klingons_left);
			default:
				//should not occur
		}
	}
	fmt.Println(srs_1);

	return;
}

const lrs_1 string = "-------------------\n";

func put1bcd(v uint16) {
	v &= 0x0F;
	//putchar('0' + v);
	fmt.Println("0" + string(v))
}

func putbcd(x uint16) {
	put1bcd(x >> 8);
	put1bcd(x >> 4);
	put1bcd(x);
}

func long_range_scan() {
	var i, j uint16;
	var y1, y2 uint16
	var x1, x2 uint16

	if (inoperable(3)) {
		return;
	}

	fmt.Printf("Long Range Scan for Quadrant %d, %d\n\n", quad_y, quad_x);

	y1 = quad_y - 1
	y2 = quad_y + 1
	x1 = quad_x - 1
	x2 = quad_x + 1
	for i = y1; i <= y2; i++ {
		fmt.Printf("%s:", lrs_1);
		for j = x1 ; j <= x2; j++ {
			fmt.Print(' ');
			if (i > 0 && i <= 8 && j > 0 && j <= 8) {
				gmap[i][j] |= MAP_VISITED;
				putbcd(gmap[i][j]);
			} else {
				fmt.Print("***");
			}
			fmt.Print(" :");
		}
		fmt.Print('\n');
	}

	fmt.Printf("%s\n", lrs_1);
}

func no_klingon() bool {
	if (klingons <= 0) {
		fmt.Println("Science Officer Spock reports:")
		fmt.Println("  'Sensors show no enemy ships in this quadrant'");
		return true;
	}
	return false;
}

func wipe_klingon(k *klingon) {
	quad[k.y - 1][k.x - 1] = Q_SPACE;
}

func phaser_control() {
	var i uint16;
	var phaser_energy uint16;
	var h1 uint16;
	var h uint16;
	//struct klingon *k = kdata;
	var k *klingon

	if (inoperable(4)) {
		return;
	}

	if (no_klingon()) {
		return;
	}

	/* There's Klingons on the starboard bow... */
	if (damage[8] < 0) {
		fmt.Println("Computer failure hampers accuracy.");
	}

	fmt.Println("Phasers locked on target;")
	fmt.Printf("Energy available = %d units\n\n", energy);
	fmt.Println("Number of units to fire: ");

	phaser_energy = input_int();

	if (phaser_energy <= 0) {
		return;
	}

	if (energy - phaser_energy < 0) {
		fmt.Println("Not enough energy available.");
		return;
	}

	energy -=  phaser_energy;

	/* We can fire up to nearly 3000 points of energy so we do this
	   bit in 32bit math */

	if (damage[8] < 0) {
		phaser_energy *= get_rand(100);
	} else {
		phaser_energy *= 100;
	}

	h1 = phaser_energy / klingons;

	for i = 0; i <= 2; i++ {
		k = kdata[i]
		if (k.energy > 0) {
			/* We are now 32bit with four digits accuracy */
			h = h1 * (get_rand(100) + 200);
			/* Takes us down to 2 digit accuracy */

			h /= distance_to(k);

			if (h <= 15 * k.energy) {	/* was 0.15 */
				fmt.Printf("Sensors show no damage to enemy at %d, %d\n\n", k.y, k.x);
			} else {
				h = FROM_FIXED00(h);
				k.energy -= h;
				fmt.Printf("%d unit hit on Klingon at sector %d, %d\n", h, k.y, k.x);
				if (k.energy <= 0) {
					fmt.Println("*** Klingon Destroyed ***");
					klingons--;
					klingons_left--;
					wipe_klingon(k);
					k.energy = 0;
					/* Minus a Klingon.. */
					gmap[quad_y][quad_x] -= 0x100;
					if (klingons_left <= 0) {
						won_game();
					}
				} else {
					fmt.Printf("   (Sensors show %d units remaining.)\n\n", k.energy);
				}
			}
		}
		//k++;
	}

	klingons_shoot();
}

func photon_torpedoes() {
	var x3, y3 uint16;
	var c1 uint16;
	var c2, c3, c4 uint16;
	var x, y uint16
	var x1, x2 int16;

	if (torps <= 0) {
		fmt.Println("All photon torpedoes expended");
		return;
	}

	if (inoperable(5)) {
		return;
	}

	fmt.Println("Course (0-9): ");
	c1 = input_f00();

	if (c1 == 900) {
		c1 = 100;
	}

	if (c1 < 100 || c1 >= 900) {
		fmt.Println("Ensign Chekov reports:\n  Incorrect course data, sir!");
		return;
	}

	/* FIXME: energy underflow check ? */
	energy = energy - 2;
	torps--;

	c2 = FROM_FIXED00(c1);	/* Integer part */
	c3 = c2 + 1;		/* Next integer part */
	c4 = (c1 - TO_FIXED00(c2));	/* Fractional element in fixed point */

	x1 = 100 * c[1][c2] + (c[1][c3] - c[1][c2]) * int16(c4);
	x2 = 100 * c[2][c2] + (c[2][c3] - c[2][c2]) * int16(c4);

	/* The basic code is very confused about what is X and what is Y */
	//x1 and x2 can theoretically be negative
	x = uint16(int16(ship_y) + x1);
	y = uint16(int16(ship_x) + x2);

	x3 = FROM_FIXED00(x);
	y3 = FROM_FIXED00(y);

	fmt.Println("Torpedo Track:");

	//while (x3 >= 1 && x3 <= 8 && y3 >= 1 && y3 <= 8) {
	for (x3 >= 1 && x3 <= 8 && y3 >= 1 && y3 <= 8) {
		var p uint16;

		fmt.Printf("    %d, %d\n", x3, y3);

		p = quad[x3-1][y3-1];
		/* In certain corner cases the first trace we'll step is
		   ourself. If so treat it as space */
		if (p != Q_SPACE && p != Q_SHIP) {
			torpedo_hit(x3, y3);
			klingons_shoot();
			return;
		}

		x = uint16(int16(x) + x1);
		y = uint16(int16(y) + x2);

		x3 = FROM_FIXED00(x);
		y3 = FROM_FIXED00(y);
	}

	fmt.Println("Torpedo Missed\n");

	klingons_shoot();
}

func torpedo_hit(yp uint16, xp uint16) {
	var i uint16;
	var k *klingon
	
	switch(quad[yp-1][xp-1]) {
	case Q_STAR:
		fmt.Printf("Star at %d, %d absorbed torpedo energy.\n\n", yp, xp);
		return;
	case Q_KLINGON:
		fmt.Println("*** Klingon Destroyed ***");
		klingons--;
		klingons_left--;

		if (klingons_left <= 0) {
			won_game();
		}

		//k = kdata;
		for i = 0; i <= 2; i++ {
			k = kdata[i]
			if (yp == k.y && xp == k.x) {
				k.energy = 0;
			}
			//k++;
		}
		gmap[quad_y][quad_x] -= 0x100;
		break;
	case Q_BASE:					
		fmt.Println("*** Starbase Destroyed ***");
		starbases--;
		starbases_left--;

		if (starbases_left <= 0 && klingons_left <= FROM_FIXED(stardate) - time_start - time_up) {
			/* showfile ? FIXME */
			fmt.Println("That does it, Captain!!")
			fmt.Println("You are hereby relieved of command")
			fmt.Println("and sentenced to 99 stardates of hard")
			fmt.Println("labor on Cygnus 12!!");
			resign_commision();
		}

		fmt.Println("Starfleet Command reviewing your record to consider court martial!");

		docked = 0;		/* Undock */
		gmap[quad_y][quad_x] -= 0x10;
		break;
	}
	quad[yp-1][xp-1] = Q_SPACE;
}

func damage_control() {
	var repair_cost uint16 = 0;
	var i uint16;
	var absdmg uint16

	if (damage[6] < 0) {
		fmt.Println("Damage Control report not available.");
	}

	/* Offer repair if docked */
	if (docked==1) {
		/* repair_cost is x.xx fixed point */
		repair_cost = 0;
		for i = 1; i <= 8; i++ {
			if (damage[i] < 0) {
				repair_cost = repair_cost + 10;
			}
		}

		if (repair_cost>0) {
			repair_cost = repair_cost + d4;
			if (repair_cost >= 100) {
				repair_cost = 90;	/* 0.9 */
			}

			fmt.Println("\nTechnicians standing by to effect repairs to your")
			fmt.Printf("ship;\nEstimated time to repair: %s stardates.\n", print100(repair_cost))
			fmt.Println("Will you authorize the repair order (y/N)? ");

			if (yesno()) {
				for i = 1; i <= 8; i++ {
					if (damage[i] < 0) {
						damage[i] = 0;
					}
				}

				/* Work from two digit to one digit. We might actually
				   have to give in and make t a two digt offset from
				   a saved constant base only used in printing to
				   avoid that round below FIXME */
				stardate += (repair_cost + 5)/10 + 1;
			}
			return;
		}
	}

	if (damage[6] < 0) {
		return;
	}

	fmt.Println("Device            State of Repair");

	for i = 1; i <= 8; i++ {
		if (damage[i] < 0 ) {
			absdmg = uint16(0 - damage[i])
		} else {
			absdmg = uint16(damage[i])	
		}
		fmt.Printf("%-25s%6s\n", get_device_name(i), print100(absdmg));
	}
}

func shield_control() {
	var i uint16;

	if (inoperable(7)) {
		return;
	}

	fmt.Printf("Energy available = %d\n\n",energy + shield)
	fmt.Println("Input number of units to shields: ");

	i = input_int();

	if (i < 0 || shield == i) {
//unchanged:
		fmt.Println("<Shields Unchanged>\n");
		return;
	}

	if (i >= energy + shield) {
		fmt.Println("Shield Control Reports:\n")
		fmt.Println("  'This is not the Federation Treasury.'");
		fmt.Println("<Shields Unchanged>\n");
		//goto unchanged;
		return
	}

	energy = energy + shield - i;
	shield = i;

	fmt.Println("Deflector Control Room report:\n")
	fmt.Printf("  'Shields now at %d units per your command.'\n\n", shield);
}

func library_computer() {

	if (inoperable(8)) {
		return;
	}

	fmt.Println("Computer active and awating command: ");

	switch(input_int()) {
		/* -1 means 'typed nothing or junk */
		case 65535:
			break;
		case 0:
			galactic_record();
			break;
		case 1:
			status_report();
			break;
		case 2:
			torpedo_data();
			break;
		case 3:
			nav_data();
			break;
		case 4:
			dirdist_calc();
			break;
		case 5:
			galaxy_map();
			break;
		default:
			/* FIXME: showfile */
			fmt.Println("Functions available from Library-Computer:")
			fmt.Println("   0 = Cumulative Galactic Record")
			fmt.Println("   1 = Status Report")
			fmt.Println("   2 = Photon Torpedo Data")
			fmt.Println("   3 = Starbase Nav Data")
			fmt.Println("   4 = Direction/Distance Calculator")
			fmt.Println("   5 = Galaxy 'Region Name' Map");
	}
}

func galactic_record() {
	var i, j uint16;

	fmt.Printf("\n     Computer Record of Galaxy for Quadrant %d,%d\n\n", quad_y, quad_x);
	fmt.Println("     1     2     3     4     5     6     7     8");

	for i = 1; i <= 8; i++ {
		fmt.Print("   ----- ----- ----- ----- ----- ----- ----- -----");
		fmt.Print(i);

		for j = 1; j <= 8; j++ {
			fmt.Print("   ");

			if ( (gmap[i][j] & MAP_VISITED) > 0) {
				putbcd(gmap[i][j]);
			} else {
				fmt.Print("***");
			}
		}
		fmt.Print('\n');
	}
	fmt.Println("   ----- ----- ----- ----- ----- ----- ----- -----");
}

func status_report() {
	var plural string
	//const char *plural = str_s + 1;
	var left uint16 = TO_FIXED(time_start + time_up) - stardate;

	fmt.Println("   Status Report:\n");

	if (klingons_left > 1) {
		plural = "s";
	}

	/* Assumes fixed point is single digit fixed */
	fmt.Printf("Klingon%s Left: %d\n Mission must be completed in %d.%d stardates\n",plural, klingons_left,
		FROM_FIXED(left), left%10);

	if (starbases_left < 1) {
		fmt.Println("Your stupidity has left you on your own in the galaxy")
		fmt.Println(" -- you have no starbases left!");
	} else {
		plural = "s";
		//if (starbases_left < 2) {
		//	plural++;
		//}
		fmt.Printf("The Federation is maintaining %d starbase%s in the galaxy\n\n", starbases_left, plural);
	}
}

func torpedo_data() {
	var i int;
	//const char *plural = str_s + 1;
	//var plural string
	//struct klingon *k;
	var k *klingon

	/* Need to also check sensors here ?? */
	if (no_klingon()) {
		return;
	}

	//if (klingons > 1) {
	//	plural--;
	//}

	fmt.Println("From Enterprise to Klingon battlecruiser:")

	//k = kdata;
	for i = 0; i <= 2; i++ {
		k = kdata[i]
		if (k.energy > 0) {
			compute_vector(TO_FIXED00(k.y),TO_FIXED00(k.x),ship_y, ship_x);
		}
		//k++;
	}
}

func nav_data() {
	if (starbases <= 0) {
		fmt.Println("Mr. Spock reports,")
		fmt.Println("  'Sensors show no starbases in this quadrant.'");
		return;
	}
	compute_vector(TO_FIXED00(base_y), TO_FIXED00(base_x), ship_y, ship_x);
}

/* Q: do we want to support fractional co-ords ? */
func dirdist_calc() {
	var c1, a, w1, x uint16;
	fmt.Println("Direction/Distance Calculator")
	fmt.Printf("You are at quadrant %d,%d sector %d,%d",quad_y, quad_x,FROM_FIXED00(ship_y), FROM_FIXED00(ship_x));
	fmt.Println("Please enter initial X coordinate: ")

	c1 = TO_FIXED00(input_int());
	if (c1 < 0 || c1 > 900 ) {
		return;
	}

	fmt.Println("Please enter initial Y coordinate: ");
	a = TO_FIXED00(input_int());
	if (a < 0 || a > 900) {
		return;
	}

	fmt.Println("Please enter final X coordinate: ");
	w1 = TO_FIXED00(input_int());
	if (w1 < 0 || w1 > 900) {
		return;
	}

	fmt.Println("Please enter final Y coordinate: ");
	x = TO_FIXED00(input_int());
	if (x < 0 || x > 900) {
		return;
	}
	compute_vector(w1, x, c1, a);
}

func galaxy_map() {
	var i, j, j0 uint16;
	var tmp uint16

	fmt.Println("\n                   The Galaxy\n\n");
	fmt.Println("    1     2     3     4     5     6     7     8\n");

	for i = 1; i <= 8; i++ {
		//printf("%s%d ", gm_1, i);
		fmt.Print("  ----- ----- ----- ----- ----- ----- ----- ----- ")
		fmt.Println(i)

		quadname = quadrant_name(1, i, 1);

		j0 = uint16(11 - (len(quadname) / 2));

		for j = 0; j < j0; j++ {
			fmt.Print(' ');
		}

		fmt.Print(quadname);

		for j = 0; j < j0; j++ {
			fmt.Print(' ');
		}

		tmp = uint16(len(quadname) % 2)
		if (tmp == 0) {
			fmt.Print(' ');
		}

		//quadrant_name(1, i, 5);
		quadname = quadrant_name(1, i, 5);

		j0 = uint16(12 - (len(quadname) / 2));

		for j = 0; j < j0; j++ {
			fmt.Print(' ');
		}

		fmt.Print(quadname);
	}

	//puts(gm_1);
	fmt.Println("  ----- ----- ----- ----- ----- ----- ----- ----- ")
}

//static const char *dist_1 = "  DISTANCE = %s\n\n";

func abs(x uint16) uint16 {
	if (x < 0 ) {
		return 0 - x
	} else {
		return x
	}
}

//FIX THIS
//just put debug statements in
func compute_vector(w1 uint16, x uint16, c1 uint16, a uint16) {
	var x1, a1 uint16;
	var tmp uint16

	fmt.Print("  DIRECTION = ")
	/* All this is happening in fixed point */
	x = x - a;
	a = c1 - w1;

	x1 = abs(x);
	a1 = abs(a);

	if (x < 0) {
		if (a > 0) {
			c1 = 300;
//estimate2:
		/* Multiply the top half by 100 to keep in fixed0 */
			if (a1 >= x1) {
				fmt.Printf("%s", print100(c1 + ((x1 * 100) / a1)));
			} else {
				fmt.Printf("%s", print100(c1 + ((((x1 * 2) - a1) * 100)  / x1)));
			}
			if x > a { tmp = x} else {tmp = a}
			fmt.Printf("  DISTANCE = %s\n\n", print100(tmp));
			return;
		} else if (x != 0){
			c1 = 500;
			fmt.Println("ERRROR: goto estimate1;")
			return;
		} else {
			c1 = 700;
			fmt.Println("ERRROR: goto estimate2;")
		}
	} else if (a < 0) {
		c1 = 700;
		fmt.Println("ERRROR: goto estimate2;")
	} else if (x > 0) {
		c1 = 100;
		fmt.Println("ERRROR: goto estimate1;")
	} else if (a == 0) {
		c1 = 500;
		fmt.Println("ERRROR: goto estimate1;")
	} else {
		c1 = 100;
//estimate1:
		/* Multiply the top half by 100 as well so that we keep it in fixed00
		   format. Our larget value is int 9 (900) so we must do this 32bit */
		if a1 <= x1 {
			fmt.Printf("%s", print100(c1 + ((a1 * 100) / x1)));
		} else {
			fmt.Printf("%s", print100(c1 + ((((a1 * 2) - x1) * 100) / a1)));
		}
		if x1 > a1 {
			tmp = x1
		} else { 
			tmp = a1
		}
		fmt.Printf("  DISTANCE = %s\n\n", print100(tmp));
	}
}

func ship_destroyed() {
	fmt.Println("The Enterprise has been destroyed. ")
	fmt.Println("The Federation will be conquered.");

	end_of_time();
}

func end_of_time() {
	fmt.Printf("It is stardate %d.\n\n",  FROM_FIXED(stardate));

	resign_commision();
}

func resign_commision() {
	fmt.Printf("There were %d Klingon Battlecruisers left at the end of your mission.\n\n", klingons_left);

	end_of_game();
}

func won_game() {
	fmt.Println("Congratulations, Captain!  The last Klingon Battle Cruiser")
	fmt.Println("menacing the Federation has been destoyed.");

	if (FROM_FIXED(stardate) - time_start > 0) {
		fmt.Printf("Your efficiency rating is %s\n",
			print100(square00(TO_FIXED00(total_klingons)/(FROM_FIXED(stardate) - time_start))));
		// 1000 * pow(total_klingons / (float)(FROM_FIXED(t) - time_start), 2));
	}
	end_of_game();
}

func end_of_game() {
	//char x[4];
	var x string
	if (starbases_left > 0) {
		/* FIXME: showfile ? */
		fmt.Println("The Federation is in need of a new starship commander")
		fmt.Println(" for a similar mission.")
		fmt.Println("If there is a volunteer, let him step forward and")
		fmt.Println(" enter 'aye': ");

		x = get_input();
		if x == "aye" {
			new_game();
		}
	}
	os.Exit(0);
}

func klingons_move() {
	var i uint16;
	//struct klingon *k = kdata;
	var k *klingon

	for i = 0; i <= 2; i++ {
		k = kdata[i]
		if (k.energy > 0) {
			wipe_klingon(k);

			//find_set_empty_place(Q_KLINGON, &k->y, &k->x);
			k.y,k.x = find_set_empty_place(Q_KLINGON);
		}
		//k++;
	}

	klingons_shoot();
}

//static const char *dcr_1 = "Damage Control report:";

func klingons_shoot() {
	var h uint16;
	var i uint16;
	var k *klingon;
	var ratio uint16
	var r uint16

	if (klingons <= 0) {
		return;
	}

	if (docked>0) {
		fmt.Println("Starbase shields protect the Enterprise\n");
		return;
	}

	for i = 0; i <= 2; i++ {
		k = kdata[i]
		if (k.energy > 0) {
			h = k.energy * (200 + get_rand(100));
			h *= 100;	/* Ready for division in fixed */
			h /= distance_to(k);
			/* Takes us back into FIXED00 */
			shield = shield - FROM_FIXED00(h);

			k.energy = (k.energy * 100) / (300 + get_rand(100));

			fmt.Printf("%d unit hit on Enterprise from sector %d, %d\n", FROM_FIXED00(h), k.y, k.x);

			if (shield <= 0) {
				fmt.Println();
				ship_destroyed();
			}

			fmt.Printf("    <Shields down to %d units>\n\n", shield);

			if (h >= 20) {
				/* The check in basic is float and is h/s >.02. We
				   have to use 32bit values here to avoid an overflow
				   FIXME: use a better algorithm perhaps ? */
				ratio = h / shield;
				if (get_rand(10) <= 6 || ratio > 2) {
					r = rand8();
					/* The original basic code computed h/s in
					   float form the C conversion broke this. We correct it in the fixed
					   point change */
					damage[r] -= int16(ratio + get_rand(50));

					/* FIXME: can we use dcr_1 here ?? */
					fmt.Printf("Damage Control reports '%s' damaged by hit\n\n", get_device_name(r));
				}
			}
		}
		//k++;
	}
}

func repair_damage(warp uint16) {
	var i uint16;
	var d1 uint16;
	var repair_factor uint16;		/* Repair Factor */
	var r uint16
	dcr_1 := "Damage Control report:"

	repair_factor = warp;
	if (warp >= 100) {
		repair_factor = TO_FIXED00(1);
	}

	for i = 1; i <= 8; i++ {
		if (damage[i] < 0) {
			damage[i] = damage[i] + int16(repair_factor);
			if (damage[i] > -10 && damage[i] < 0) {	/* -0.1 */
				damage[i] = -10;
			} else if (damage[i] >= 0) {
				if (d1 != 1) {
					d1 = 1;
					fmt.Print(dcr_1);
				}
				fmt.Printf("    %s repair completed\n\n",get_device_name(i));
				damage[i] = 0;
			}
		}
	}

	if (get_rand(10) <= 2) {
		r = rand8();

		if (get_rand(10) < 6) {
			/* Working in 1/100ths */
			damage[r] -= int16(get_rand(500) + 100);
			fmt.Println(dcr_1);
			fmt.Printf("    %s damaged\n\n", get_device_name(r));
		} else {
			/* Working in 1/100ths */
			damage[r] += int16(get_rand(300) + 100);
			fmt.Println(dcr_1);
			fmt.Printf("    %s state of repair improved\n\n",get_device_name(r));
		}
	}
}

/* Misc Functions and Subroutines
   Returns co-ordinates r1/r2 and for now z1/z2 */

//static void find_set_empty_place(uint8_t t, uint8_t *z1, uint8_t *z2)
func find_set_empty_place(t uint16) (uint16,uint16) {
	var r1, r2 uint16;
	b := true
	for b {
		r1 = rand8();
		r2 = rand8();
		b = (quad[r1-1][r2-1] != Q_SPACE )
	}
	//do {
	//	r1 = rand8();
	//	r2 = rand8();
	//} while (quad[r1-1][r2-1] != Q_SPACE );
	
	quad[r1-1][r2-1] = t;
	
	//if (z1)
	//	*z1 = r1;
	//if (z2)
	//	*z2 = r2;
	return r1,r2
}

//static const char *device_name[] = {
//	"", "Warp engines", "Short range sensors", "Long range sensors",
//	"Phaser control", "Photon tubes", "Damage control", "Shield control",
//	"Library computer"
//};

//NOTE: this uses int as input, because this is commonly used with a loop
func get_device_name(n uint16) string {
	if (n < 0 || n > 8) { n = 0; }
	return device_name[n];
}

//static const char *quad_name[] = { 
//};
var quad_name = [...]string {"",
	"Antares", "Rigel", "Procyon", "Vega", "Canopus", "Altair",
	"Sagittarius", "Pollux", "Sirius", "Deneb", "Capella",
	"Betelgeuse", "Aldebaran", "Regulus", "Arcturus", "Spica"}

//this sets the global variable quadname
//how about just return it
func quadrant_name(small uint16, y uint16, x uint16) string {
	var q string

	//static char *sect_name[] = { "", " I", " II", " III", " IV" };
	var sect_name = [5]string { "", " I", " II", " III", " IV" }

	if (y < 1 || y > 8 || x < 1 || x > 8) {
		return "Unknown";
	}

	if (x <= 4) {
		q = quad_name[y];
	} else {
		q = quad_name[y + 8];
	}

	if (small != 1) {
		if (x > 4) {
			x = x - 4;
		}
		q = sect_name[x];
	}

	return q;
}

/* An unsigned sqrt is all we need.
   What we are actually doing here is a smart version of calculating n^2
   repeatedly until we find the right one */
func isqrt(i uint16) uint16 {
	var b uint16 = 0x4000 
	var q uint16 = 0 
	var r uint16 = i 
	var t uint16 = 0;
	for b>0 {
		t = q + b;
		q >>= 1;
		if (r >= t) {
			r -= t;
			q += b;
		}
		b >>= 2;
	}
	return q;
}

func square00(t uint16) uint16 {
	if (abs(t) > 181) {
		t /= 10;
		t *= t;
	} else {
		t *= t;
		t /= 100;
	}
	return t;
}

/* Return the distance to an object in x.xx fixed point */
func distance_to(k *klingon) uint16 {
	var j uint16;

	/* We do the squares in fixed point maths */
	j = square00(TO_FIXED00(k.y) - ship_y);
	j += square00(TO_FIXED00(k.x) - ship_x);

	/* Find the integer square root */
	j = isqrt(j);
	/* Correct back into 0.00 fixed point */
	j *= 10;

	return j;
}


/* Round off floating point numbers instead of truncating */
//static int cint100(int16_t d)
//{
//	return (d + 50) / 100;
//}
func cint100(d uint16) uint16 {
	return (d + 50) / 100;
}

//static void showfile(char *filename)
//{
//	FILE *fp;
//	char buffer[MAXCOL];
//	int row = 0;
//
//	fp = fopen(filename, "r");
//	if (fp == NULL) {
//		perror(filename);
//		return;
//	}
//	while (fgets(buffer, sizeof(buffer), fp) != NULL) {
//		fputs(buffer, stdout);
//		if (row++ > MAXROW - 3) {
//			getchar();
//			row = 0;
//		}
//	}
//	fclose(fp);
//}

func showfile(filename string) {
    file, err := os.Open(filename)
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        fmt.Println(scanner.Text())
    }

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}