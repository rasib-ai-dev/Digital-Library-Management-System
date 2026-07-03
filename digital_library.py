import streamlit as st

class Book():
    def __init__ (self, title, author, book_id, total_copies):
        self.__title = title
        self.__author = author
        self.__book_id = book_id
        self.__total_copies = total_copies
        self.__available_copies = total_copies

    def availability_check(self):
        if self.__available_copies > 0:
            return True
        else:
            return False 

    def borrow_copy(self):
        if self.__available_copies > 0:
            self.__available_copies -= 1
        
    def return_copy(self):
        if self.__available_copies < self.__total_copies:
            self.__available_copies += 1

    def to_dict(self):
        return {
        "Title": self.__title,
        "Author": self.__author,
        "Book ID": self.__book_id,
        "Total copies": self.__total_copies,
        "Available copies": self.__available_copies
    }


class Library():
    def __init__(self):
        self.books = {}
        self.borrowed_books = {}

        self.add_book("Python Basics", "John Smith", "B001", 5)
        self.add_book("Data Science", "Andrew Ng", "B002", 3)
        self.add_book("Machine Learning", "Tom Mitchell", "B003", 4)
        self.add_book("Artificial Intelligence", "Stuart Russell", "B004", 2)
        self.add_book("Deep Learning", "Ian Goodfellow", "B005", 6)
        self.add_book("Python Advanced", "Mark Lutz", "B006", 4)
        self.add_book("Data Analysis with Python", "Wes McKinney", "B007", 5)
        self.add_book("AI for Beginners", "Tom Taulli", "B008", 3)
        self.add_book("Statistics Essentials", "David Freedman", "B009", 6)
        self.add_book("Neural Networks", "Simon Haykin", "B010", 2)


    def add_book(self, title, author, book_id, total_copies):
        if book_id in self.books:
            return False
        else:
            book = Book(title, author, book_id, total_copies)
            self.books[book_id] = book
            return True

    def search_book_by_title(self, title):
        matching_books = []
        for book in self.books.values():
            if book.to_dict()["Title"].lower() == title.lower():
                matching_books.append(book.to_dict())
        return matching_books

    def borrow_book(self, book_id, name):
        if book_id in self.books:
            if self.books[book_id].availability_check():
                self.books[book_id].borrow_copy()
                if book_id in self.borrowed_books:
                    self.borrowed_books[book_id].append(name)
                else:
                    self.borrowed_books[book_id] = [name]
                return True
        return False


    def return_book(self, book_id, name):
        if book_id in self.borrowed_books:
            if name in self.borrowed_books[book_id]:
                self.books[book_id].return_copy()
                self.borrowed_books[book_id].remove(name)
                if not self.borrowed_books[book_id]:
                    del self.borrowed_books[book_id]
                return True
        return False

    def search_book_by_author(self, author):
        matching_books = []
        for book in self.books.values():
            if book.to_dict()["Author"].lower() == author.lower():
                matching_books.append(book.to_dict())
        return matching_books

    def view_all_books(self):
        return [book.to_dict() for book in self.books.values()]

    def view_borrowed_books(self):
        borrowed_list = []
        for book_id, names in self.borrowed_books.items():
            title = self.books[book_id].to_dict()["Title"]
            borrowed_list.append({"Book": title, "Borrowed by": ", ".join(names)})
        return borrowed_list

st.set_page_config(page_title="SMIT DIGITAL LIBRARY")
st.title("SMIT DIGITAL LIBRARY")
st.markdown("Welcome to SMIT Digital Library")

if 'library' not in st.session_state:
    st.session_state.library = Library()
library = st.session_state.library


option = st.sidebar.selectbox(
    "Choose an action",
    ["Add Book", "Search by Title", "Search by Author", 
     "Borrow Book", "Return Book", "View All Books", "View Borrowed Books"]
)

if option == "Add Book":
    with st.form("add_book_form"):
        add_title = st.text_input("Book Title")
        add_author = st.text_input("Author Name")
        add_book_id = st.text_input("Book ID")
        add_total_copies = st.number_input("Total Copies", min_value=1, step=1)
        submitted = st.form_submit_button("Add Book")
        if submitted:
            success = library.add_book(add_title, add_author, add_book_id, add_total_copies)
            if success:
                st.success("Book added successfully")
            else:
                st.error("Book ID already exists")


elif option == "Search by Title":
    with st.form("search_title_form"):
        search_title = st.text_input("Enter Book Title")
        submitted = st.form_submit_button("Search by Title")
        if submitted:
            result = library.search_book_by_title(search_title)
            if result:
                st.table(result)
            else:
                st.error("Book not found")

elif option == "Search by Author":
    with st.form("search_author_form"):
        search_author = st.text_input("Enter Author Name")
        submitted = st.form_submit_button("Search by Author")
        if submitted:
            result = library.search_book_by_author(search_author)
            if result:
                st.table(result)
            else:
                st.error("No books found by this author")


elif option == "Borrow Book":
    with st.form("borrow_book_form"):
        borrow_book_id = st.text_input("Book ID to Borrow")
        borrow_name = st.text_input("Your Name")
        submitted = st.form_submit_button("Borrow Book")
        if submitted:
            success = library.borrow_book(borrow_book_id, borrow_name)
            if success:
                st.success("Book borrowed successfully")
            else:
                st.error("Cannot borrow this book")


elif option == "Return Book":
    with st.form("return_book_form"):
        return_book_id = st.text_input("Book ID to Return")
        return_name = st.text_input("Your Name")
        submitted = st.form_submit_button("Return Book")
        if submitted:
            success = library.return_book(return_book_id, return_name)
            if success:
                st.success("Book returned successfully")
            else:
                st.error("Cannot return this book")


elif option == "View All Books":
    books_list = library.view_all_books()
    if books_list:
        st.table(books_list)
    else:
        st.info("No books available in the library")


elif option == "View Borrowed Books":
    borrowed_list = library.view_borrowed_books()
    if borrowed_list:
        st.table(borrowed_list)
    else:
        st.info("No borrowed books currently")
