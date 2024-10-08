from modules.checkpoint import get_checkpoint_data, load_checkpoint, save_checkpoint
from modules.scrapper import get_movie_items, extract_data
from modules.processor import convert_to_dict
from modules.loader import save_data

if __name__ == '__main__':

    proceed = True
    page = 3 # have you ever try with more pages ? How about 10
    new_checkpoint_data = set()
    total_movie_data = []
    current_checkpoint_data = load_checkpoint()
    
    while(proceed):

        print(page)
        movie_items = get_movie_items(page)
        for movie in movie_items:

            checkpoint_data = get_checkpoint_data(movie)

            # Check if the movie item has ben processed on the previous batch or not
            if checkpoint_data in current_checkpoint_data:
                save_checkpoint(new_checkpoint_data)  # Save this batch as checkpoint for future scrapping batches
                proceed = False  # Stop this movie item processing batch
                break  

            new_checkpoint_data.add(checkpoint_data)

            movie_data = extract_data(movie)
            if len(movie_data) == 0:  # Skip to next movie in case there is no data
                continue

            total_movie_data.append(convert_to_dict(id=checkpoint_data[0], data=movie_data))
            print(movie_data)

        page += 1
        if page > 3:
            proceed = False

    save_data(total_movie_data)