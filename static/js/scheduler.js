/// <reference path="MindFusion.Scheduling-vsdoc.js" /> 

var p = MindFusion.Scheduling;

// create a new instance of the calendar
calendar = new p.Calendar(document.getElementById("calendar"));

// set the view to Timetable, which displays the allotment of resources to distinct hours of a day
calendar.currentView = p.CalendarView.Timetable;

calendar.theme = "pastel";
calendar.contactNameFormat = "F L";
calendar.timetableSettings.startTime = 420;
calendar.timetableSettings.endTime = 1260;
calendar.timetableSettings.titleFormat = "dddd d MMM yyyy";
calendar.itemSettings.tooltipFormat = "%s[hh:mm tt] - %e[hh:mm tt] %h (Contact: %d)";

var resource;

// Add some contacts to the schedule.contacts collection.
resource = new p.Contact();
resource.firstName = "Dr. Bryan";
resource.lastName = "Stephenson";
resource.tag = 0;
calendar.schedule.contacts.add(resource);

resource = new p.Contact();
resource.firstName = "Dr. David";
resource.lastName = "Smith";
resource.tag = 1;
calendar.schedule.contacts.add(resource);

resource = new p.Contact();
resource.firstName = "Dr. Lora";
resource.lastName = "Patterson";
resource.tag = 2;
calendar.schedule.contacts.add(resource);

resource = new p.Contact();
resource.firstName = "Dr. Michael";
resource.lastName = "Brown";
resource.tag = 3;
calendar.schedule.contacts.add(resource);

// Add some locations to the schedule.locations collection.
resource = new p.Location();
resource.name = "Room 102";
calendar.schedule.locations.add(resource);

resource = new p.Location();
resource.name = "Room 105";
calendar.schedule.locations.add(resource);

resource = new p.Location();
resource.name = "Room 112";
calendar.schedule.locations.add(resource);

resource = new p.Location();
resource.name = "Room 127";
calendar.schedule.locations.add(resource);

// group the calendar
group(p.GroupType.GroupByContacts);

// render the calendar control
calendar.render();

datePicker = new p.Calendar(document.getElementById("datePicker"));
datePicker.currentView = p.CalendarView.List;

datePicker.theme = "pastel";
datePicker.listSettings.visibleCells = datePicker.listSettings.numberOfCells = 30;
datePicker.listSettings.headerStyle = p.MainHeaderStyle.None;
datePicker.listSettings.generalFormat = "ddd d";
datePicker.useForms = false;
datePicker.selectionEnd.addEventListener(handleSelectionEnd);
datePicker.render();
//make the selection of the control is rendered
datePicker.selection.setRange(p.DateTime.today(), p.DateTime.today().addDays(1));

function handleSelectionEnd(sender, args) {
	var startDate = args.startTime;
	var endDate = args.endTime;

	// show the selected date range in the timetable
	calendar.timetableSettings.dates.clear();
	while (startDate < endDate) {
		calendar.timetableSettings.dates.add(startDate);
		startDate = p.DateTime.addDays(startDate, 1);
	}
}

// attach handler
calendar.itemCreated.addEventListener(handleItemCreated);
calendar.itemCreating.addEventListener(handleItemCreating);

function handleItemCreating(sender, args)
{
	var appLocation = args.item.location;
	
	if(appLocation != null )
	{
		if(appLocation.name != "")
		{
			var items = calendar.schedule.items.items();
			for(var i = 0; i < calendar.schedule.items.count(); i++)
			{
				if( items[i].location == null)
					continue;
				
				//if the location is the same as the location of another appointment
				//at that time we cancel the creating of the appointment
				if( items[i].location.name == appLocation.name && 
				overlappingAppointments (args.item, items[i]))
				{
					args.cancel = true;
					alert("The room is already taken");
				}
	
			}
		}
	}
}

/* checks if the time allotted to two different appointments overlaps */
function overlappingAppointments(item1, item2)
{
	if( item1.startTime < item2.startTime &&
	    item1.endTime < item2.endTime )
		  return false;
		  
	if( item1.startTime > item2.endTime &&
	    item1.endTime > item2.endTime )
		  return false;	
		  
		  return true;	  		
}

function handleItemCreated(sender, args)
{
	var contact = args.item.contacts.items()[0];
	
	if(contact != null )
		args.item.cssClass = "itemClass" + contact.tag;
}


function group(value) {
	calendar.contacts.clear();
	if (value == p.GroupType.GroupByContacts) {
		// add the contacts by which to group to the calendar.contacts collection
		calendar.contacts.addRange(calendar.schedule.contacts.items());
	}
	calendar.locations.clear();
	if (value == p.GroupType.GroupByLocations) {
		// add the locations by which to group to the calendar.locations collection
		calendar.locations.addRange(calendar.schedule.locations.items());
	}
	calendar.groupType = value;
}

calendar.visibleDateChanged.addEventListener(

	function (sender, args)
	{
		datePicker.selection.setRange(args.newDate);
	}
)