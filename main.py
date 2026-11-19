
from dataclasses import dataclass
from drafter import *

set_website_title("Watchlist")
set_site_information(
    author="Wehlo Simms",
    description="Add movies and shows to track what you've watched!",
    sources="Thanks to the Drafter docs and my course work.",
    planning=["https://docs.google.com/document/d/1ne1lEWRHgwh4AUwr8miETM7Pp6D1J2WSRLeEDPrWdgU/edit?tab=t.0#heading=h.1xxqmmg350hh", "https://docs.google.com/document/d/1tzi4JPFsE7yW56Y22uJ45Qc3PDXD1GL2rFH11wVolJg/edit?tab=t.0#heading=h.1xxqmmg350hh"],
    links=[]
)
hide_debug_information()
set_website_framed(False)

@dataclass
class MovieShow:
    id: int
    title: str
    kind: str
    genre: str


@dataclass
class State:
    watchlist: list[MovieShow]
    selected_genre: str
    search_results: list[int]
    message: str
    selected_kind: str
    next_id: int


@route
def index(state: State) -> Page:
    return Page([
        Header("Welcome to WatchList!"),
        "Keep track of your movies and TV shows.\n",
        Button("Add a Title", add_title),
        Button("View My Collection", view_collection),
        Button("Search by Genre", genre_search),
        Button("Filter by Type", filter_by_kind)
    ])


@route
def add_title(state: State) -> Page:
    return Page(state, [
        "Add a Movie or TV Show",
        TextBox("title"),
        SelectBox("kind", ["Movie", "TV Show"]),
        SelectBox("genre", [
            "Action", "Comedy", "Drama", "Horror", "Sci-Fi"
        ]),
        Button("Add to Collection", save_title),
        Button("Home", index)
    ])


@route
def save_title(state: State, title: str, kind: str, genre: str) -> Page:
    if title.strip() == "":
        state.message = "Please enter a title."
    else:
        new_title = MovieShow(
            state.next_id,
            title.strip(),
            kind,
            genre
        )
        state.watchlist.append(new_title)
        state.next_id += 1
        state.message = title + " was added successfully!"

    return Page(state, [
        state.message,
        Button("Add Another Title", add_title),
        Button("View Collection", view_collection),
        Button("Home", index)
    ])


@route
def view_collection(state: State) -> Page:
    contents = ["My Collection"]

    if len(state.watchlist) == 0:
        contents.append("Your collection is empty. Add a title!")
    else:
        for item in state.watchlist:
            contents.append(item.title)
            contents.append(item.kind + " | " + item.genre)
            contents.append(
                Button(
                    "Remove " + item.title,
                    remove_title,
                    arguments={"movie_id": item.id}
                )
            )

    contents.append(Button("Home", index))
    return Page(state, contents)


@route
def genre_search(state: State) -> Page:
    return Page(state, [
        "Search by Genre",
        SelectBox("genre", [
            "Action", "Comedy", "Drama", "Horror", "Sci-Fi"
        ]),
        Button("Search", show_genre_results),
        Button("Home", index)
    ])


@route
def show_genre_results(state: State, genre: str) -> Page:
    state.selected_genre = genre
    state.search_results = []

    for item in state.watchlist:
        if item.genre == genre:
            state.search_results.append(item.id)

    contents = ["Search Results for " + genre]

    if len(state.search_results) == 0:
        contents.append("No titles found in this genre.")
    else:
        for movie_id in state.search_results:
            for item in state.watchlist:
                if item.id == movie_id:
                    contents.append(item.title)
                    contents.append(item.kind)

    contents.append(Button("Search Another Genre", genre_search))
    contents.append(Button("View Collection", view_collection))
    contents.append(Button("Home", index))

    return Page(state, contents)


@route
def filter_by_kind(state: State) -> Page:
    return Page(state, [
        "Filter by Type",
        SelectBox("kind", ["Movie", "TV Show"]),
        Button("Show Titles", show_kind_results),
        Button("Home", index)
    ])


@route
def show_kind_results(state: State, kind: str) -> Page:
    state.selected_kind = kind
    contents = ["Your " + kind + " Collection"]

    found = False

    for item in state.watchlist:
        if item.kind == kind:
            contents.append(item.title + " | " + item.genre)
            found = True

    if not found:
        contents.append("No titles found.")

    contents.append(Button("View All Titles", view_collection))
    contents.append(Button("Home", index))

    return Page(state, contents)


@route
def remove_title(state: State, movie_id: int) -> Page:
    found = False

    for item in state.watchlist:
        if item.id == movie_id:
            state.message = item.title + " was removed."
            state.watchlist.remove(item)
            found = True
            break

    if not found:
        state.message = "That title could not be found."

    return Page(state, [
        state.message,
        Button("View Collection", view_collection),
        Button("Home", index)
    ])


start_server(State([], "", [], "", "", 1))
