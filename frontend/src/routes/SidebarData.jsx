import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'; 
import { faTachometerAlt, faClockRotateLeft, faBook, faUser, faLightbulb, faDisplay } from '@fortawesome/free-solid-svg-icons'; 
import { faRaspberryPi } from '@fortawesome/free-brands-svg-icons';

export const SidebarData = [
    {
        title: "Home",
        icon: <FontAwesomeIcon icon={faTachometerAlt} />, 
        link: "/",
    },
    {
        title: "History",
        icon: <FontAwesomeIcon icon={faClockRotateLeft} />, 
        link: "/history"
    },
    {
        title: "Books",
        icon: <FontAwesomeIcon icon={faBook} />, 
        link: "/books"
    },
    {
        title: "Users",
        icon: <FontAwesomeIcon icon={faUser} />, 
        link: "/users"
    },
    {
        title: "Rasps",
        icon: <FontAwesomeIcon icon={faDisplay}/>, 
        link: "/rasps"
    },
    {
        title: "Devices",
        icon: <FontAwesomeIcon icon={faLightbulb} />, 
        link: "/devices"
    }
];