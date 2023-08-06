"""
If you use LibAUC in your works, please cite our papers. 
"""
import torch 
import torch.nn.functional as F

class AUCMLoss(torch.nn.Module):
    """
    AUCM Loss with squared-hinge function: a novel loss function to directly optimize AUROC
    
    inputs:
        margin: margin term for AUCM loss, e.g., m in [0, 1]
        imratio: imbalance ratio, i.e., the ratio of number of postive samples to number of total samples
    outputs:
        loss value 
    
    Reference: 
        Yuan, Z., Yan, Y., Sonka, M. and Yang, T., 
        Large-scale Robust Deep AUC Maximization: A New Surrogate Loss and Empirical Studies on Medical Image Classification. 
        International Conference on Computer Vision (ICCV 2021)
    Link:
        https://arxiv.org/abs/2012.03173
    """
    def __init__(self, margin=1.0, imratio=None):
        super(AUCMLoss, self).__init__()
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.margin = margin
        self.p = imratio
        # https://discuss.pytorch.org/t/valueerror-cant-optimize-a-non-leaf-tensor/21751
        self.a = torch.zeros(1, dtype=torch.float32, device=self.device, requires_grad=True).to(self.device) #cuda()
        self.b = torch.zeros(1, dtype=torch.float32, device=self.device,  requires_grad=True).to(self.device) #.cuda()
        self.alpha = torch.zeros(1, dtype=torch.float32, device=self.device, requires_grad=True).to(self.device) #.cuda()
        
    def forward(self, y_pred, y_true):
        if self.p is None:
           self.p = (y_true==1).float().sum()/y_true.shape[0]   
     
        y_pred = y_pred.reshape(-1, 1) # be carefull about these shapes
        y_true = y_true.reshape(-1, 1) 
        loss = (1-self.p)*torch.mean((y_pred - self.a)**2*(1==y_true).float()) + \
                    self.p*torch.mean((y_pred - self.b)**2*(0==y_true).float())   + \
                    2*self.alpha*(self.p*(1-self.p)*self.margin + \
                    torch.mean((self.p*y_pred*(0==y_true).float() - (1-self.p)*y_pred*(1==y_true).float())) )- \
                    self.p*(1-self.p)*self.alpha**2
        return loss
    
    
class APLoss_SH(torch.nn.Module):
    def __init__(self, data_len=None, margin=1.0,  beta=0.99, batch_size=128):
        """
        AP Loss with squared-hinge function: a novel loss function to directly optimize AUPRC.
    
        inputs:
            margin: margin for squred hinge loss, e.g., m in [0, 1]
            beta: factors for moving average, which aslo refers to gamma in the paper
        outputs:
            loss  
        Reference:
            Qi, Q., Luo, Y., Xu, Z., Ji, S. and Yang, T., 2021. 
            Stochastic Optimization of Area Under Precision-Recall Curve for Deep Learning with Provable Convergence. 
            arXiv preprint arXiv:2104.08736.
        Link:
            https://arxiv.org/abs/2104.08736
        """
        super(APLoss_SH, self).__init__()
        self.u_all = torch.tensor([0.0]*data_len).view(-1, 1).cuda()
        self.u_pos = torch.tensor([0.0]*data_len).view(-1, 1).cuda()
        self.margin = margin
        self.beta = beta

    def forward(self, y_pred, y_true, index_s): 

        f_ps = y_pred[y_true == 1].reshape(-1, 1)
        f_ns = y_pred[y_true == 0].reshape(-1, 1)

        f_ps = f_ps.reshape(-1)
        f_ns = f_ns.reshape(-1)

        vec_dat = torch.cat((f_ps, f_ns), 0)
        mat_data = vec_dat.repeat(len(f_ps), 1)

        f_ps = f_ps.reshape(-1, 1)

        neg_mask = torch.ones_like(mat_data)
        neg_mask[:, 0:f_ps.size(0)] = 0

        pos_mask = torch.zeros_like(mat_data)
        pos_mask[:, 0:f_ps.size(0)] = 1

        neg_loss = torch.max(self.margin - (f_ps - mat_data), torch.zeros_like(mat_data)) ** 2 * neg_mask
        pos_loss = torch.max(self.margin - (f_ps - mat_data), torch.zeros_like(mat_data)) ** 2 * pos_mask
        loss = pos_loss + neg_loss

        if f_ps.size(0) == 1:
            self.u_pos[index_s] = (1 - self.beta) * self.u_pos[index_s] + self.beta * (pos_loss.mean())
            self.u_all[index_s] = (1 - self.beta) * self.u_all[index_s] + self.beta * (loss.mean())
        else:
            self.u_all[index_s] = (1 - self.beta) * self.u_all[index_s] + self.beta * (loss.mean(1, keepdim=True))
            self.u_pos[index_s] = (1 - self.beta) * self.u_pos[index_s] + self.beta * (pos_loss.mean(1, keepdim=True))

        p = (self.u_pos[index_s] - (self.u_all[index_s]) * pos_mask) / (self.u_all[index_s] ** 2)

        p.detach_()
        loss = torch.sum(p * loss)
        loss = loss.mean()
        return loss
 
    
class CrossEntropyLoss(torch.nn.Module):
    """
    Cross Entropy Loss with Sigmoid Function
    Reference: 
        https://pytorch.org/docs/stable/generated/torch.nn.BCEWithLogitsLoss.html
    """
    def __init__(self):
        super(CrossEntropyLoss, self).__init__()
        self.criterion = F.binary_cross_entropy_with_logits  # with sigmoid

    def forward(self, y_pred, y_true):
        return self.criterion(y_pred, y_true)
    
    
class FocalLoss(torch.nn.Module):
    """
    Focal Loss
    Reference: 
        https://amaarora.github.io/2020/06/29/FocalLoss.html
    """
    def __init__(self, alpha=.25, gamma=2):
        super(FocalLoss, self).__init__()
        self.alpha = torch.tensor([alpha, 1-alpha]).cuda()
        self.gamma = gamma

    def forward(self, inputs, targets):
        BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduction='none')
        targets = targets.type(torch.long)
        at = self.alpha.gather(0, targets.data.view(-1))
        pt = torch.exp(-BCE_loss)
        F_loss = at*(1-pt)**self.gamma * BCE_loss
        return F_loss.mean()

    
    