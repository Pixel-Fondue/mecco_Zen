#perl
#BY: Seneca Menard
#version 1.1
#This script is to select similar polygons.  There's four different uses and one slider:
#selectByPoly = This is to select all (similar facing) touching polygons.  (faster, but less accurate than selectTouching)
#selectTouching = This is to select all (similar facing) touching polygons. (more accurate, but slower than selectByPoly)
#selectOnObject = This is to select all (similar facing) polygons on an object.
#selectAll = This is to select all (similar facing) polygons in the entire layer.
#--------------------------
#facingRatio = This is to tell the script exactly how similar the polygons you want it to select should be.
#-(8-11-07 bugfix) The script won't select hidden polys anymore.

lxout("SELECT SIMILAR POLYGONS SCRIPT---------------------------------");

#setup variables
my $mainlayer = lxq("query layerservice layers ? main");
my @originalPolys = lxq("query layerservice polys ? selected");
my @matchingPolys;
my %normalList;
my $count;
my $pi = 3.14159265358979323;
#safety check
if (lxq("select.count polygon ?") == 0)	{	lxout("There were no polys selected so I'm killing the script");	return;} #hrmm.  that seems to work.


#------------------------------------------------------------------------------------------------------------
#USER VARIABLES
#------------------------------------------------------------------------------------------------------------
#create the sene_LS_facingRatio variable if it didn't already exist.
if (lxq("query scriptsysservice userValue.isdefined ? sene_LS_facingRatio") == 0)
{
	lxout("-The sene_LS_facingRatio cvar didn't exist so I just created one");
	lx("user.defNew sene_LS_facingRatio float");
	lx("user.def sene_LS_facingRatio username Facing_Ratio");
	lx("user.def sene_LS_facingRatio min 0");
	lx("user.def sene_LS_facingRatio max 180");
	lx("user.value sene_LS_facingRatio 10");
}

#create the sene_LS_accuracy variable if it didn't already exist.
if (lxq("query scriptsysservice userValue.isdefined ? sene_LS_accuracy") == 0)
{
	lxout("-The sene_LS_accuracy cvar didn't exist so I just created one");
	lx("user.defNew sene_LS_accuracy float");
	lx("user.def sene_LS_accuracy username Accuracy");
	lx("user.def sene_LS_accuracy min 0");
	lx("user.def sene_LS_accuracy max 90");
	lx("user.value sene_LS_accuracy 10");
}

#facing ratio
my $facingRatio = lxq("user.value sene_LS_facingRatio ?");
$facingRatio = $facingRatio*($pi/180);	#convert angle to radian.
$facingRatio = cos($facingRatio);		#convert radian to DP.
#lxout("-facingRatio = $facingRatio");

#accuracy
my $accuracy = lxq("user.value sene_LS_accuracy ?");
$accuracy = $accuracy*($pi/180);	#convert angle to radian.
$accuracy = cos($accuracy);		#convert radian to DP.
#lxout("-accuracy = $accuracy");

#------------------------------------------------------------------------------------------------------------
#ARGS
#------------------------------------------------------------------------------------------------------------
foreach my $arg (@ARGV)
{
	if ($arg eq "selectByPoly")		{	our $selectByPoly = 1;		}
	if ($arg eq "selectTouching")	{	our $selectTouching = 1;	}
	if ($arg eq "selectOnObject")	{	our $selectOnObject = 1;	}
	if ($arg eq "selectAll")		{	our $selectAll = 1;			}
}



#------------------------------------------------------------------------------------------------------------
#RUN SCRIPT NOW
#------------------------------------------------------------------------------------------------------------
foreach my $arg (@ARGV)
{
	if 		($selectByPoly == 1)	{	&selByPolyLoop;								}
	elsif	($selectTouching == 1)	{	&originalPolyNormList;	&selectTouching;	}
	elsif 	($selectOnObject == 1)	{	&originalPolyNormList;	&selectOnObject;	}
	elsif 	($selectAll == 1)		{	&originalPolyNormList;	&selectAll;			}
}



#------------------------------------------------------------------------------------------------------------
#BUILD THE ORIGINAL POLY NORMAL LIST
#------------------------------------------------------------------------------------------------------------
sub originalPolyNormList
{
	lxout("[->] ORIGINAL POLY NORMAL LIST subroutine");

	#throw the first selected poly into the list to generate the table.
	my @firstPolyNormal = lxq("query layerservice poly.normal ? @originalPolys[0]");
	$normalList{"@firstPolyNormal[0] @firstPolyNormal[1] @firstPolyNormal[2]"}[0] = @firstPolyNormal[0];
	$normalList{"@firstPolyNormal[0] @firstPolyNormal[1] @firstPolyNormal[2]"}[1] = @firstPolyNormal[1];
	$normalList{"@firstPolyNormal[0] @firstPolyNormal[1] @firstPolyNormal[2]"}[2] = @firstPolyNormal[2];

	#build the array of selected Polys' normals
	foreach my $poly (@originalPolys)
	{
		my @normal = lxq("query layerservice poly.normal ? $poly");

		#I have to look thru the entire hash table for any similar keys.  If there aren't any, I have to add this normal to the table.
		my $loopCount = keys %normalList;
		my $i = 1;
		foreach my $key (keys %normalList)
		{
			my $dp = ((@normal[0]*$normalList{$key}[0])+(@normal[1]*$normalList{$key}[1])+(@normal[2]*$normalList{$key}[2]));			#lxout("normalDiff = @normalDiff");
			#lxout("poly($poly) <> (round $i)  <><> normal($key) <><> dp($dp)");

			#if the normal's basically already in the table, throw it away.
			if ($dp > $accuracy)
			{
				last;
			}
			#if it's the last round and it still hasn't found anything, add it to the list.
			elsif ($i == $loopCount)
			{
				#lxout("poly($poly) <> It's the last round, and it still hasn't found a similar normal, so i'm adding it to the list");
				$normalList{"@normal[0] @normal[1] @normal[2]"}[0] = @normal[0];
				$normalList{"@normal[0] @normal[1] @normal[2]"}[1] = @normal[1];
				$normalList{"@normal[0] @normal[1] @normal[2]"}[2] = @normal[2];
			}
			#if it's not in the table and it's not the last round, then go to the next round.
			else
			{
				$i++;
			}
		}
	}

	my $hashNumber = scalar(keys %normalList);
	lxout("--There are $hashNumber unique poly normals selected");
	lxout("--Accuracy = $accuracy");
	lxout("--FacingRatio = $facingRatio");
}



#------------------------------------------------------------------------------------------------------------
#SELECT BY POLY SETUP sub
#------------------------------------------------------------------------------------------------------------
sub selByPolyLoop
{
	#This tool is a very fast+cheap way to select similar.   It doesn't build a normal table, it just uses the first poly normal per set.
	lxout("[->] SELBYPOLYLOOP subroutine");

	#build polygons hash table
	our $expandPolyLoop = 1;
	our %selByPolyTable;
	our @polygons = lxq("query layerservice polys ? selected");
	foreach my $poly (@polygons)
	{
		$selByPolyTable{$poly}  = 1;
	}

	#run the expand poly loop until there's none left.
	while ($expandPolyLoop == 1)
	{
		my @selByPolyTableArray = (keys %selByPolyTable);
		@originalPolys = @selByPolyTableArray[0];

		#lxout("-Working on poly (@originalPolys[0])");
		my @normal = lxq("query layerservice poly.normal ? @originalPolys[0]");
		$normalList{@originalPolys[0]}[0] = @normal[0];
		$normalList{@originalPolys[0]}[1] = @normal[1];
		$normalList{@originalPolys[0]}[2] = @normal[2];

		&selectTouching;
		%normalList = ();
	}
}



#------------------------------------------------------------------------------------------------------------
#SELECT TOUCHING SIMILAR POLYGONS sub
#------------------------------------------------------------------------------------------------------------
sub selectTouching
{
	lxout("[->] SELECT TOUCHING subroutine");
	my $stopScript = 0;
	our %totalPolyList;
	my %currentPolys;
	my @lastPolyList;
	my $i = 0;

	#--------------------------------------------------------
	#SETUP----------------------------------------------
	#--------------------------------------------------------
	if ($selectByPoly == 0)
	{
		foreach my $poly (@originalPolys)		{	$totalPolyList{$poly} = 1;		}
		#foreach my $key (keys %totalPolyList)	{ 	lxout("total poly list = $key");	}
	}
	else
	{
		#lxout("-Clearing the total poly list");
		%totalPolyList =();
	}
	@lastPolyList = @originalPolys;


	#--------------------------------------------------------
	#SIMILAR POLY FIND+SELECT LOOP------
	#--------------------------------------------------------
	while ($stopScript == 0)
	{
		#[1] : LOOK at verts of current poly list and convert 'em into previously unselected polys.
		my %vertList;
		foreach my $poly (@lastPolyList)
		{
			my @verts = lxq("query layerservice poly.vertList ? $poly");

			foreach my $vert (@verts)
			{
				if ($vertList{$vert} == "")
				{
					#lxout("This vert wasn't in the vert list ($vert)");
					$vertList{$vert} = 1;
				}
			}
		}
		#my @sortedVertList = sort keys(%vertList);
		#lxout("(%)vertList = @sortedVertList");


		#[2] : LOOK at the polys on the verts and ignore the ones that are in the totalPolyList
		foreach my $vert (keys %vertList)
		{
			my @polys = lxq("query layerservice vert.polyList ? $vert");
			#lxout("vert ($vert) polys = @polys");

			foreach my $poly (@polys)
			{
				if (lxq("query layerservice poly.hidden ? $poly") == 0)
				{
					if ($totalPolyList{$poly} == "")
					{
						#only add the poly to the list if it's not in there.
						if ($currentPolys{$poly} == "")
						{
							#lxout("This poly ($poly) was not in the total Poly list ");
							$currentPolys{$poly} = 1;
						}
					}
				}
			}
		}
		#my @sortedCurrentPolys = sort keys(%currentPolys);
		#lxout("(%)currentPolys = @sortedCurrentPolys");



		#[3] : LOOK at each currentPoly normal and see if it matches. if so, add to total list and last list
		foreach my $poly (keys %currentPolys)
		{
			my @normal = lxq("query layerservice poly.normal ? $poly");
			foreach my $key(keys %normalList)
			{
				my $dp = ((@normal[0]*$normalList{$key}[0])+(@normal[1]*$normalList{$key}[1])+(@normal[2]*$normalList{$key}[2]));
				#lxout("poly($poly) <><> normal($key) <><> dp = $dp");
				if ($dp >= $facingRatio)
				{
					#lxout("---This poly $poly is close enough to the facing ratio");
					push(@matchingPolys,$poly);
					last;
				}
			}
		}
		#lxout("-matchingPolys = @matchingPolys");



		#[4] : SELECT the matching polygons
		for (my $i =0; $i<@matchingPolys; $i++){ 	lx("select.element $mainlayer polygon add @matchingPolys[$i]"); 	}



		#[6] : Tell the script whether to continue looping or not.
		if ($#matchingPolys == -1)
		{
			#lxout("-There are NO matching polys left, so I'm killing the loop");
			$stopScript = 1;
		}



		#[5] : Update the poly lists
		foreach my $poly (keys %currentPolys)	{	$totalPolyList{$poly} = 1;		}

		#Update the poly lists for the EXPAND POLY SUB
		if ($selectByPoly == 1)
		{
			#remove the matching polys from the loop list
			delete $selByPolyTable{@originalPolys[0]};
			foreach my $poly (@matchingPolys)
			{
				#lxout("-deleting $poly");
				delete $selByPolyTable{$poly};
			}

			#if the loop list has no polys in it, kill the loop
			my $selByPolyTableCount = scalar(keys(%selByPolyTable));
			if (($selByPolyTableCount == 0) && ($expandPolyLoop == 1))
			{
				$expandPolyLoop = 0;
			}
		}
		@lastPolyList = @matchingPolys;
		@matchingPolys = ();
		%currentPolys = ();
	}
}






#------------------------------------------------------------------------------------------------------------
#SELECT ALL SIMILAR POLYS ON ENTIRE OBJECT sub
#------------------------------------------------------------------------------------------------------------
sub selectOnObject
{
	lxout("[->] SELECT ON OBJECT subroutine");

	#select rest to get rest of polygons on objects
	lx("select.connect");
	my @connectedPolys = lxq("query layerservice polys ? selected");

	#go thru connected polys and find which are similar
	foreach my $poly (@connectedPolys)
	{
		#ignore the original poly List
		if ((grep(/\b$poly\b/, @originalPolys)) == 1)
		{
			next;
		}
		else
		{
			#lxout("$poly getting thru existing sel check-----------------------");
			my @normal = lxq("query layerservice poly.normal ? $poly");
			foreach my $key(keys %normalList)
			{
				my $dp = ((@normal[0]*$normalList{$key}[0])+(@normal[1]*$normalList{$key}[1])+(@normal[2]*$normalList{$key}[2]));
				#lxout("poly($poly) <><> normal($key) <><> dp = $dp");
				if ($dp >= $facingRatio)
				{
					#lxout("---This poly $poly is close enough to the facing ratio");
					push(@matchingPolys,$poly);
					last;
				}
			}
		}
	}
	#lxout("matchingPolys = @matchingPolys");

	#now select the polygons that were close enough
	lx("select.drop polygon");
	for (my $i =0; $i<@originalPolys; $i++) 	{ 	lx("select.element $mainlayer polygon add @originalPolys[$i]"); 	}
	for (my $i =0; $i<@matchingPolys; $i++){ 	lx("select.element $mainlayer polygon add @matchingPolys[$i]"); 	}
}



#------------------------------------------------------------------------------------------------------------
#SELECT ALL SIMILAR POLYGONS IN LAYER subroutine
#------------------------------------------------------------------------------------------------------------
sub selectAll
{
	lxout("[->] SELECT ALL SIMILAR subroutine");

	#drop selection
	lx("select.drop polygon");
	lx("select.invert");

	#build the TOTAL poly list in layer.
	my @totalPolys = lxq("query layerservice polys ? selected");

	#drop the poly selection and only select similar polys.
	lx("select.drop polygon");
	foreach my $poly (@totalPolys)
	{
		my @normal = lxq("query layerservice poly.normal ? $poly");
		#lxout("normal = @normal");
		foreach my $key(keys %normalList)
		{
			my $dp = ((@normal[0]*$normalList{$key}[0])+(@normal[1]*$normalList{$key}[1])+(@normal[2]*$normalList{$key}[2]));
			#lxout("poly($poly)=@normal[0],@normal[1],@normal[2] <><> normal($key) <><> dp = $dp <><> FR=$facingRatio");
			if ($dp >= $facingRatio)
			{
				#lxout("---This poly $poly is close enough to the facing ratio");
				lx("select.element $mainlayer polygon add $poly");
				last;
			}
		}
	}
}






##********************************************************************************
##****************************SUBROUTINES***********************************
##********************************************************************************
sub popup
{
	lx("dialog.setup yesNo");
	lx("dialog.msg {@_}");
	lx("dialog.open");
	my $confirm = lxq("dialog.result ?");
	if($confirm == "0"){die;}
	#if($confirm eq "no"){die;}	#TEMP
}
