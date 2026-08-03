import torch


def save_checkpoint(

    model,

    optimizer,

    epoch,

    best_acc,

    path

):

    torch.save(

        {

            "epoch": epoch,

            "model_state_dict":

                model.state_dict(),

            "optimizer_state_dict":

                optimizer.state_dict(),

            "best_acc": best_acc

        },

        path

    )