import h5py
import argparse

from keras.models import Sequential
from keras.layers import Dense

from dlgo.agent.predict import DeepLearningAgent, load_prediction_agent
from dlgo.data.parallel_processor import GoDataProcessor
from dlgo.encoders.sevenplane import SevenPlaneEncoder
# from dlgo.httpfrontend import get_web_app
from dlgo.networks import large

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bot-name', help="Name of the bot. <bot-name>_bot.h5 will be the name of the file.", default="default")
    parser.add_argument('--optimizer', help="Type of optimizer. Default: adadelta", default="adadelta")
    parser.add_argument('--epochs', help="The amount of epochs to train. Default: 10", type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=128)
    parser.add_argument('--num-samples', help="Number of samples to train from. MINIMUM: 50", type=int, default=100)

    args = parser.parse_args()
    if args.num_samples < 50:
        print("ERROR: Please use a sample size greater than 50!")
        exit(1)
    go_board_rows, go_board_cols = 19, 19
    nb_classes = go_board_rows * go_board_cols
    encoder = SevenPlaneEncoder((go_board_rows, go_board_cols))
    processor = GoDataProcessor(encoder=encoder.name())
    # generator = processor.load_go_data('train', args.num_samples, use_generator=True)
    # test_generator = processor.load_go_data('test', args.num_samples, use_generator=True)

    X, y = processor.load_go_data(num_samples=args.num_samples)

    input_shape = (encoder.num_planes, go_board_rows, go_board_cols)
    model = Sequential()
    network_layers = large.layers(input_shape)
    for layer in network_layers:
        model.add(layer)
    model.add(Dense(nb_classes, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=args.optimizer, metrics=['accuracy'])

    model.fit(X, y, batch_size=args.batch_size, epochs=args.epochs, verbose=1)

    deep_learning_bot = DeepLearningAgent(model, encoder)
    try:
        deep_learning_bot.serialize(h5py.File("./agents/{}_bot.h5".format(args.bot_name)))
        print("Saving {}_bot.h5 to agents/".format(args.bot_name))
    except ValueError as e:
        print(e)
        new_name = input("Please enter a different name :  ")
        deep_learning_bot.serialize(h5py.File("./agents/{}_bot.h5".format(new_name)))
        print("Saving {}_bot.h5 to agents/".format(new_name))


    # model_file = h5py.File("./agents/deep_bot_3.h5", "r")
    # bot_from_file = load_prediction_agent(model_file)

    # web_app = get_web_app({'predict': bot_from_file})
    # web_app.run()
