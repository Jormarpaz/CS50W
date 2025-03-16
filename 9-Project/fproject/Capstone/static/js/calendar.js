document.addEventListener("DOMContentLoaded", function () {
    var calendarEl = document.getElementById("calendar");
    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      },
      initialView: "dayGridMonth",
      editable: true,
      selectable: true,
      unselectAuto: true,
      events: [
      ],
      dateClick: function (info) {
        var events = calendar.getEvents().filter((event) => {
          return event.startStr.startsWith(info.dateStr);
        });

        // Crear contenedor para mostrar los eventos
        var eventsContainer = document.createElement("div");
        eventsContainer.id = "events-container";
        eventsContainer.innerHTML = `
                    <h3>Eventos del día ${info.dateStr}</h3>
                    <ul>
                        ${
                          events.length > 0
                            ? events
                                .map(
                                  (event) => `
                                <li>
                                    <strong>${event.title}</strong> <span style="margin-left: 5px;"><a href="#" onclick="editEvent('${event.id}')"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
  <path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"/>
  <path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"/>
</svg></a></span><br>
                                    ${
                                      event.allDay
                                        ? "Todo el día"
                                        : event.end
                                        ? `De ${event.start.toLocaleTimeString(
                                            [],
                                            {
                                              hour: "2-digit",
                                              minute: "2-digit",
                                            }
                                          )} a ${event.end.toLocaleTimeString(
                                            [],
                                            {
                                              hour: "2-digit",
                                              minute: "2-digit",
                                            }
                                          )}`
                                        : `A partir de la/s ${event.start.toLocaleTimeString(
                                            [],
                                            {
                                              hour: "2-digit",
                                              minute: "2-digit",
                                            }
                                          )}`
                                    }
                                </li>
                            `
                                )
                                .join("")
                            : "<li>No hay eventos para este día.</li>"
                        }
                    </ul>
                    <button class="btn btn-primary" onclick="showEventForm('${
                      info.dateStr
                    }')">Añadir evento</button>
                    <button class="btn btn-secondary" onclick="document.body.removeChild(this.parentElement)">Cerrar</button>
                `;
        eventsContainer.style.position = "fixed";
        eventsContainer.style.top = "50%";
        eventsContainer.style.left = "50%";
        eventsContainer.style.transform = "translate(-50%, -50%)";
        eventsContainer.style.backgroundColor = "white";
        eventsContainer.style.padding = "20px";
        eventsContainer.style.border = "1px solid #ccc";
        eventsContainer.style.borderRadius = "5px";
        eventsContainer.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
        eventsContainer.style.zIndex = "1000";

        document.body.appendChild(eventsContainer);
      },
    });
    calendar.render();

    window.showEventForm = function (dateStr) {
      // Cerrar el contenedor de eventos si existe
      var eventsContainer = document.getElementById("events-container");
      if (eventsContainer) {
        document.body.removeChild(eventsContainer);
      }

      // Mostrar el formulario
      var form = document.getElementById("event-form");
      form.style.display = "block";

      // Prellenar la fecha seleccionada
      document.getElementById("event-start").value = "";
      document.getElementById("event-end").value = "";

      form.onsubmit = function (event) {
        event.preventDefault();
        var title = document.getElementById("event-title").value;
        var start = document.getElementById("event-start").value;
        var end = document.getElementById("event-end").value;
        var allDay = document.getElementById("event-all-day").checked;

        if (title) {
          calendar.addEvent({
            title: title,
            start: allDay ? dateStr : dateStr + "T" + start,
            end: allDay ? null : dateStr + "T" + end,
            allDay: allDay,
          });
        }
        calendar.unselect();
        form.style.display = "none";
      };
    };

    window.editEvent = function (eventId) {
      var event = calendar.getEventById(eventId);
      if (event) {
        // Cerrar el contenedor de eventos si existe
        var eventsContainer = document.getElementById("events-container");
                if (eventsContainer) {
                    document.body.removeChild(eventsContainer);
                }
        
        var form = document.getElementById("event-form");
        form.style.display = "block";
        document.getElementById("event-title").value = event.title;
        document.getElementById("event-start").value = event.start
          .toISOString()
          .substring(11, 16);
        document.getElementById("event-end").value = event.end
          ? event.end.toISOString().substring(11, 16)
          : "";
        document.getElementById("event-all-day").checked = event.allDay;

        form.onsubmit = function (e) {
          e.preventDefault();
          var title = document.getElementById("event-title").value;
          var start = document.getElementById("event-start").value;
          var end = document.getElementById("event-end").value;
          var allDay = document.getElementById("event-all-day").checked;
          if (title) {
            event.setProp("title", title);
            event.setStart(
              allDay
                ? event.startStr.split("T")[0]
                : event.startStr.split("T")[0] + "T" + start
            );
            event.setEnd(
              allDay ? null : event.startStr.split("T")[0] + "T" + end
            );
            event.setAllDay(allDay);
          }
          form.style.display = "none";
        };
      }
    };
  });
