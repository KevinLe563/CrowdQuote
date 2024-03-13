import numpy as np
import copy
import matplotlib.pyplot as plt

def hierarchical_cluster(initial_clusters, termination_threshold=200):
    print(initial_clusters)
    print("*" * 10)
    clusters = []
    for k, v in initial_clusters.items():
        clusters.append(v)

    best_k = len(initial_clusters)
    best_fitness = 0
    best_clusters = copy.deepcopy(clusters)
    while len(clusters) > 0:  # silhouette <= avg
        # plot clusters
        print(f"Current K: {len(clusters)}")
        # if len(clusters) < 15:
        #     plot_clusters(clusters)

        fitness = evaluate_k_fitness(clusters)

        if fitness > best_fitness:
            best_k = len(clusters)
            best_fitness = fitness
            best_clusters = copy.deepcopy(clusters)

        if len(clusters) == 1:
            break

        # min = float(inf)
        # c1, c2 = None, None <- c1 and c2 are indices
        # for i ...
        # for j in i ...
        #   if dist < min -> replace c1, c2, min

        # append c2 to c1, delete c2

        min_dist = float("inf")
        c1, c2 = None, None

        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                mean1 = mean_of_cluster(clusters[i])
                mean2 = mean_of_cluster(clusters[j])

                dist = euclid_distance_between_points(mean1, mean2)

                if dist < min_dist:
                    min_dist = dist
                    c1 = i
                    c2 = j

        clusters[c1].extend(clusters[c2])
        clusters.pop(c2)

    plot_best_silhouette_score(best_clusters)
    plot_clusters(best_clusters)

    # convert best_clusters to {index: list_of_points}
    best_cluster_dict = {
        str(index): sublist for index, sublist in enumerate(best_clusters)
    }
    return best_k, best_cluster_dict

def plot_clusters(clusters):
    for i, cluster in enumerate(clusters):
        x = [p[0] for p in cluster]
        y = [p[1] for p in cluster]
        plt.scatter(x, y, label=i)

    # Adding labels and legend
    plt.xlabel("X axis")
    plt.ylabel("Y axis")
    plt.title("Points color-coded by class")
    plt.legend()

    # Show plot
    plt.grid(True)
    plt.gca().invert_yaxis()
    plt.show()

def mean_of_cluster(cluster):  # [[[x,y], []], []]
    # cluster : [[x, y], [x, y]]
    # do mean of all points in the clsuter
    return np.mean(cluster, axis=0)

# def euclid_distance_between_points(p1, p2):
#      return np.sqrt((p1[0]- p2[0])**2 + (p1[1]- p2[1])**2)

def euclid_distance_between_points(p1, p2):
    return np.sqrt(sum(np.square(np.array(p1) - np.array(p2))))

def mse_of_cluster(cluster):
    mean = mean_of_cluster(cluster)
    return np.sum(np.square(cluster - mean))  # /len(cluster)

def silhouette_score_for_each_point_in_cluster(cluster, cluster_index, means):
    sil_scores = []
    for point in cluster:
        # calc
        # find a, b
        a = euclid_distance_between_points(means[cluster_index], point)
        b = float("inf")
        for i, mean in enumerate(means):
            if i == cluster_index:
                continue
            dist = euclid_distance_between_points(mean, point)
            b = min(dist, b)

        if b == float("inf"):
            sil_scores.append(0)
        else:
            sil_score = (b - a) / (max(a, b))
            sil_scores.append(sil_score)

    return sil_scores

def evaluate_k_fitness(clusters):
    means = [mean_of_cluster(cluster) for cluster in clusters]
    # [[sil1 (sil score for point1 in cluster 1), sil2, sil3], [], []]
    all_cluster_scores = [
        silhouette_score_for_each_point_in_cluster(cluster, i, means)
        for i, cluster in enumerate(clusters)
    ]
    
    flattened = []
    for cluster_sil in all_cluster_scores:
        flattened.extend(np.array(cluster_sil).flatten())

    red_line = np.mean(np.array(flattened))
    if len(clusters) <= 15 and len(clusters) % 5 == 0:
        plot_silhouette_scores(all_cluster_scores)

    fitness = fitness_function_for_all_cluster_silhouettes(all_cluster_scores, red_line)

    return fitness

def plot_best_silhouette_score(clusters):
    means = [mean_of_cluster(cluster) for cluster in clusters]
    all_cluster_scores = [
        silhouette_score_for_each_point_in_cluster(cluster, i, means)
        for i, cluster in enumerate(clusters)
    ]
    plot_silhouette_scores(all_cluster_scores)

def plot_silhouette_scores(cluster_scores):
    # print(cluster_scores)
    flattened = []
    for cluster_sil in cluster_scores:
        flattened.extend(np.array(cluster_sil).flatten())

    avg_sil_score = np.mean(np.array(flattened))
    fig, ax = plt.subplots()
    bar_width = 0.2
    max_values = max(len(cluster) for cluster in cluster_scores)
    cluster_width = bar_width * max_values + 0.2

    for i, scores in enumerate(cluster_scores):
        scores.sort(reverse=True)
        start_index = cluster_width * i
        index = np.linspace(start_index, start_index + (len(scores)-1)*bar_width, len(scores))
        ax.barh(index, scores, bar_width, label=f"Cluster {i}")

    clusters = [f'Cluster {i+1}' for i in range(len(cluster_scores))]
    yticks_pos = [i * cluster_width for i in range(len(cluster_scores))]
    ax.set_yticks(yticks_pos)
    ax.set_yticklabels(clusters)


    # Set the x-axis and y-axis labels
    ax.set_xlabel('Silhouette Coefficient Values')
    ax.set_ylabel('Cluster Labels')
    plt.axvline(avg_sil_score, color="red", linestyle="--")
    ax.invert_yaxis() 
    plt.title(f"Silhouette scores for k={len(cluster_scores)}")
    plt.tight_layout()
    plt.show()

def fitness_function_for_all_cluster_silhouettes(all_cluster_scores, avg):
    # count number of points past line
    counts = []
    for cluster_score in all_cluster_scores:
        cluster_score_np = np.array(cluster_score)
        cluster_count = np.count_nonzero(cluster_score_np > avg)
        counts.append(cluster_count)
        if cluster_count == 0:
            # reject
            return -1

    # update the best k
    return sum(counts)

# To find sill score: given means for every class.
# a = distance of point to its mean, known which cluster
# b = distance of point to closest cluster not own, loop over means except self, get smallest dist
# plot (optional)
# avg sill score of all points
# for each cluster, count/sum/avg every point past avg line
# if a cluster has a point not past avg, reject
# else pick the k with most points past/most area/most area divided by # classes
a = {"0": [[1, 2]], "1": [[1, 3]], "2": [[1, 4]]}
a_prime = {
    "0": [[2391, 1151]],
    "1": [[2623, 1670]],
    "2": [[3897, 2006]],
    "3": [[2912, 1105]],
    "4": [[2262, 286]],
    "5": [[2722, 403]],
    "6": [[1889, 1218]],
    "7": [[1694, 274]],
    "8": [[2494, 2572]],
    "9": [[2244, 1080]],
    "10": [[2064, 1259]],
    "11": [[1696, 585]],
    "12": [[1747, 852]],
    "13": [[2387, 2128]],
    "14": [[2317, 542]],
    "15": [[2883, 166]],
    "16": [[2538, 952]],
    "17": [[2393, 182]],
    "18": [[1951, 413]],
    "19": [[1973, 117]],
    "20": [[2111, 320]],
    "21": [[2477, 148]],
    "22": [[2111, 584]],
    "23": [[2468, 372]],
    "24": [[3407, 1714]],
    "25": [[2323, 224]],
    "26": [[2316, 1938]],
    "27": [[2943, 112]],
    "28": [[2590, 329]],
    "29": [[2488, 935]],
    "30": [[2638, 138]],
    "31": [[2439, 341]],
    "32": [[1731, 2731]],
}
b = [0, 0]
c = [1, 1]


# print(mean_of_cluster(a))
# print(euclid_distance_between_clusters(b, c))
# print("hi")

# print(hierarchical_cluster(a_prime))

# # print(mse_of_cluster(a))


# import numpy as np

# # Number of points in each cluster
# num_points = 10

# # Define cluster centers and radii
# cluster_centers = np.array([[3, 3], [3, 3], [7, 7], [7, 8], [11, 3]])
# cluster_radii = np.array([2, 1, 2.5, 6, 3])

# # Generate random points within clusters
# clusters = {}
# for i, center in enumerate(cluster_centers):
#     # Generate random angles
#     angles = np.random.uniform(0, 2*np.pi, num_points)
#     # Generate random radii within cluster's radius
#     radii = np.random.uniform(0, cluster_radii[i], num_points)
#     # Calculate x-y coordinates
#     x_coords = center[0] + radii * np.cos(angles)
#     y_coords = center[1] + radii * np.sin(angles)
#     # Combine x-y coordinates into a list of points
#     points = [[x, y] for x, y in zip(x_coords, y_coords)]
#     # Add points to the dictionary with cluster name as key
#     for point in points:
#         clusters[len(clusters)] = [point]

# print(clusters)

# TO TEST UNCOMMENT THESE LINES
# clusters = {"esouihsohfsoefhi": [[2391, 1151]], 1: [[2623, 1670]], 2: [[3897, 2006]], 3: [[2912, 1105]], 4: [[2262, 286]], 5: [[2722, 403]], 6: [[1889, 1218]], 7: [[1694, 274]], 8: [[2494, 2572]], 9: [[2244, 1080]], 10: [[2064, 1259]], 11: [[1696, 585]], 12: [[1747, 852]], 13: [[2387, 2128]], 14: [[2317, 542]], 15: [[2883, 166]], 16: [[2538, 952]], 17: [[2393, 182]], 18: [[1951, 413]], 19: [[1973, 117]], 20: [[2111, 320]], 21: [[2477, 148]], 22: [[2111, 584]], 23: [[2468, 372]], 24: [[3407, 1714]], 25: [[2323, 224]], 26: [[2316, 1938]], 27: [[2943, 112]], 28: [[2590, 329]], 29: [[2488, 935]], 30: [[2638, 138]], 31: [[2439, 341]], 32: [[1731, 2731]], 33: [[2249, 2167]], 34: [[2083, 2692]], 35: [[2262, 1772]], 36: [[2088, 139]], 37: [[2838, 122]], 38: [[2819, 120]], 39: [[3302, 1453]], 40: [[2825, 581]], 41: [[2355, 960]], 42: [[2675, 357]], 43: [[3381, 2536]], 44: [[1885, 613]], 45: [[2149, 959]], 46: [[1939, 1797]], 47: [[2414, 588]], 48: [[2941, 990]], 49: [[2789, 121]], 50: [[2646, 348]], 51: [[1740, 692]]}
clusters = {'0': [[2384, 1514]]}
print(hierarchical_cluster(clusters))