# 

![Logo](/static/images/logo.png)

# Testing

Testing was ongoing throughout the entire build. We utilised Chrome developer tools while building to pinpoint and troubleshoot any issues as we went along.

### PEP8 Validator

All python files were run through PEP validator, no errors were found except:
- The links are were too long and the import has to be in the order according to the documentation.
  - [Error](/documentation/readme/images/pp8-error.png)
  - [Fix](/documentation/readme/images/pp8-fix.png)

### HTML Validator

The official [HTML validator](https://validator.w3.org/) was used to validate the HTML files. No errors were found.

  - Homepage ("/"): ![Valid](/documentation/validation/home_page.png)

  - Contact page ("/contact"): ![Valid](/documentation/validation/contact_page.png)

  - Chats list page ("/chats"): ![Valid](/documentation/validation/chats_list_page.png)

  - Chat room page ("/chats/name-of-chat"): ![Valid](/documentation/validation/chat_room_page.png)

  - Profile page ("/profile/username"): ![Valid](/documentation/validation/profile_page.png)

  - Profile edit page ("/profile/username/update"): ![Valid](/documentation/validation/profile_edit_page.png)

  - Profile delete page ("/profile/username/delete"): ![Valid](/documentation/validation/profile_delete_page.png)

  

### CSS Validator

The CSS on the site was tested using the [Jigsaw W3C CSS Validator](https://jigsaw.w3.org/css-validator/). No errors were found. There were 9 warnings regarding css variables and webkit prefixes. However, the site was perfectly functional.

![W3C validator pass](documentation/validation/css_validation.png)

### JavaScript Validator

![JSHint]()

### Lighthouse

We used Lighthouse within the Chrome Developer Tools to test the performance, accessibility, best practices and SEO of the website.

### Full Testing
To fully test the website we performed the following testing using a number of browsers (google chrome) and devices (Macbook Pro 14 inch, iPhone 13 pro).

We also went through each page using google chrome developer tools to ensure that they were responsive on all different screen sizes.

All the links in the page will open in a new tab implementing 'target="_blank"' and have been manually tested to confirm that they will direct to the correct destination.

