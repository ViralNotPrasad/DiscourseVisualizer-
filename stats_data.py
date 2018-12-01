from iacorpus import load_dataset



def load_data(dataset):
    dataset = load_dataset(dataset)
    print(dataset.dataset_metadata)


    for discussion in dataset:
        print(discussion)
        for post in discussion:
            print(post)
            exit()

def main():
    load_data("fourforums")

if __name__ == '__main__':
   main()
