
self.number_of_keywords_in_post = 0
self.keywords_found_in_post = []





if join and paymentmethods
    if self.keywords is in post
        keywords_found()
        self.join_with_payment_methods()
elif join or paymentmethods
    if join:
        # if len(self.keywords) > 0:
        if self.keywords is in post
            keywords_found()
            self.join_inclusive()
    elif paymentmethods
        if len(self.keywords) > 0:
            if self.keywords is in post
                keywords_found()
        self.payment_methods_only()
else:
    # run if keywords
    if len(self.keywords) > 0:
        if self.keywords is in post
            keywords_found()
            append_data()
    else:
        append_data()

    # else append all


def keywords_found():
    self.check_and_append_keywords(description)
    self.check_and_append_keywords(name)
    self.check_and_append_keywords(sex)
    self.check_and_append_keywords(phone_number)
    self.check_and_append_keywords(email)
    self.check_and_append_keywords(location)
    self.check_and_append_keywords(services)

def append_data(self, counter, description, email, link, location, name, phone_number, services, sex):
    self.description.append(description)
    self.name.append(name)
    self.sex.append(sex)
    self.phone_number.append(phone_number)
    self.email.append(email)
    self.location.append(location)
    self.check_for_payment_methods(description)
    self.link.append(link)
    self.post_identifier.append(counter)
    self.services.append(services)




def join_inclusive(self):
    if len(self.keywords) == len(set(self.keywords_found_in_post)):
        self.append_data(counter, description, email, link, location, name, phone_number, services,
                         sex)
        screenshot_name = str(counter) + ".png"
        self.capture_screenshot(screenshot_name)

        # strip elements from keywords_found_in_post list using comma
        self.keywords_found.append(', '.join(self.keywords_found_in_post))

        # self.keywords_found.append(self.keywords_found_in_post)
        self.number_of_keywords_found.append(self.number_of_keywords_in_post)

        counter += 1

def payment_methods_only(self):
    if self.check_for_payment_methods(description):
        self.append_data(counter, description, email, link, location, name, phone_number, services,
                         sex)
        screenshot_name = str(counter) + ".png"
        self.capture_screenshot(screenshot_name)

        # strip elements from keywords_found_in_post list using comma
        self.keywords_found.append(', '.join(self.keywords_found_in_post))

        # self.keywords_found.append(self.keywords_found_in_post)
        self.number_of_keywords_found.append(self.number_of_keywords_in_post)
        counter += 1

def join_with_payment_methods(self):
    if self.check_for_payment_methods(description) and len(self.keywords) == len(set(self.keywords_found_in_post)):
        self.append_data(counter, description, email, link, location, name, phone_number, services,
                         sex)
        screenshot_name = str(counter) + ".png"
        self.capture_screenshot(screenshot_name)

        # strip elements from keywords_found_in_post list using comma
        self.keywords_found.append(', '.join(self.keywords_found_in_post))

        # self.keywords_found.append(self.keywords_found_in_post)
        self.number_of_keywords_found.append(self.number_of_keywords_in_post)
        counter += 1