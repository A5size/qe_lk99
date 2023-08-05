import numpy as np
import matplotlib.pyplot as plt

def read_bands(filename):
    bands = []
    band  = []
    for line in open(filename):
        line = line.split()
        if len(line)==0:
            bands.append(np.array(band))
            band = []
        else:
            band.append([ float(v) for v in line ])
    return(bands)
            
def get_p_online(b1, b2, b3, kpath):
    dk = 0.0
    positions = [dk]
    for i in range(1, len(kpath)):
        ks  = kpath[i-1][0]*b1 + kpath[i-1][1]*b2 + kpath[i-1][2]*b3
        kd  = kpath[i][0]*b1 + kpath[i][1]*b2 + kpath[i][2]*b3
        v   = (kd - ks)
        dk += np.sqrt(sum(v**2))
        positions.append(dk)
    return(positions)

def get_fermi(path):
    for line in open(path):
        if "Fermi" in line:
            fermi = float(line.split()[4])
            break
    return(fermi)

def main():
    plt.rcParams["font.size"] = 18
    plt.figure(figsize=(16, 9))
    
    elec_num = (14*9 + 19*1 + 5*6 + 6*25 - 1)//2 + 1
    fermi    = get_fermi("./02nscf/out.o")
    lat_a    = 9.9306823821
    bandfile = "./04plotbands/lk99.band.gnu"
    
    b1 = np.array([0.6327042861, 0.3652919899, 0.0000000000])
    b2 = np.array([0.0000000000, 0.7305839798, 0.0000000000])
    b3 = np.array([0.0000000000, 0.0000000000, 0.8478194516])
    
    # (G, M, K, G, A, L, H, A), (L, M), (H, K, H2)
    vG  =  np.array([0.0000000000, 0.0000000000,  0.0000000000]) 
    vM  =  np.array([0.5000000000, 0.0000000000,  0.0000000000]) 
    vK  =  np.array([0.3333333333, 0.3333333333,  0.0000000000]) 
    vA  =  np.array([0.0000000000, 0.0000000000,  0.5000000000]) 
    vL  =  np.array([0.5000000000, 0.0000000000,  0.5000000000]) 
    vH  =  np.array([0.3333333333, 0.3333333333,  0.5000000000]) 
    vH2 =  np.array([0.3333333333, 0.3333333333, -0.5000000000]) 

    s1  = get_p_online(b1, b2, b3, (vG, vM, vK, vG, vA, vL, vH, vA))
    s2  = get_p_online(b1, b2, b3, (vL, vM))
    s3  = get_p_online(b1, b2, b3, (vH, vK, vH2))

    s1  = [ s/((2.0*np.pi)/lat_a) for s in s1 ]
    s2  = [ s1[-1] + s/((2.0*np.pi)/lat_a) for s in s2 ]
    s3  = [ s2[-1] + s/((2.0*np.pi)/lat_a) for s in s3 ]

    plt.axhline(y=0, color="gray", linestyle="dashed")
    for k1 in s1:
        plt.axvline(x=k1, color="gray", linestyle="dashed")
    for k2 in s2:
        plt.axvline(x=k2, color="gray", linestyle="dashed")
    for k3 in s3:
        plt.axvline(x=k3, color="gray", linestyle="dashed")

    plt.axvline(x=s1[0],  lw=3, color="dimgray", linestyle="solid")
    plt.axvline(x=s1[-1], lw=3, color="dimgray", linestyle="solid")
    plt.axvline(x=s2[-1], lw=3, color="dimgray", linestyle="solid")
    plt.axvline(x=s3[-1], lw=3, color="dimgray", linestyle="solid")

    dl = 0.08
    xticks = s1[:-1] + [s1[-1]-dl] + [s2[0]+dl] + s2[1:-1] + [s2[-1]-dl] + [s3[0]+dl] + s3[1:]
    plt.xticks(xticks, (r"$\Gamma$", "M", "K", r"$\Gamma$", "A", "L", "H", "A", "L", "M", "H", "K", r"H$_2$"))
        
    bands = read_bands(bandfile)
    for bi, band in enumerate(bands):
        if bi==elec_num-1:
            plt.plot(band[:, 0], band[:, 1]-fermi, color="red")
        else:
            plt.plot(band[:, 0], band[:, 1]-fermi, color="black")

    plt.xlim([s1[0], s3[-1]])
    plt.ylim([-2, 4])
    #plt.ylim([-0.1, 0.1])

    plt.ylabel("Energy (eV)")
    
    #plt.show()
    plt.savefig("./bands_wide.png")

if __name__=="__main__":
    main()

