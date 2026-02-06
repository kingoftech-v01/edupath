import SwiftUI

/// Course detail screen with full info and enrollment.
struct CourseDetailView: View {
    let course: Course
    @State private var reviews: [Review] = []
    @State private var isLoadingReviews = false

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 24) {
                // Hero image
                AsyncImage(url: course.imageURL) { image in
                    image
                        .resizable()
                        .aspectRatio(16/9, contentMode: .fill)
                } placeholder: {
                    Rectangle()
                        .fill(Color.gray.opacity(0.2))
                        .aspectRatio(16/9, contentMode: .fill)
                }

                VStack(alignment: .leading, spacing: 16) {
                    // Title and instructor
                    Text(course.title)
                        .font(.title)
                        .fontWeight(.bold)

                    if let instructor = course.instructor {
                        HStack {
                            AsyncImage(url: instructor.imageURL) { image in
                                image
                                    .resizable()
                                    .aspectRatio(contentMode: .fill)
                            } placeholder: {
                                Circle()
                                    .fill(Color.gray.opacity(0.2))
                            }
                            .frame(width: 40, height: 40)
                            .clipShape(Circle())

                            VStack(alignment: .leading) {
                                Text(instructor.name)
                                    .font(.headline)
                                Text(instructor.title)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }

                    // Stats
                    HStack(spacing: 24) {
                        StatItem(icon: "book", value: "\(course.lessons)", label: "Lessons")
                        StatItem(icon: "clock", value: "\(course.durationHours)h", label: "Duration")
                        StatItem(icon: "person.2", value: "\(course.students)", label: "Students")
                    }

                    Divider()

                    // Description
                    Text("About this course")
                        .font(.headline)

                    Text(course.description)
                        .font(.body)
                        .foregroundColor(.secondary)

                    // Reviews section
                    if !reviews.isEmpty {
                        Divider()

                        Text("Reviews")
                            .font(.headline)

                        ForEach(reviews) { review in
                            ReviewRow(review: review)
                        }
                    }
                }
                .padding()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
        .safeAreaInset(edge: .bottom) {
            // Enroll button
            VStack {
                Button(action: {
                    // TODO: Implement enrollment
                }) {
                    HStack {
                        Text("Enroll Now")
                            .fontWeight(.semibold)
                        Text("•")
                        Text(course.formattedPrice)
                    }
                }
                .frame(maxWidth: .infinity)
                .frame(height: 50)
                .background(Color.accentColor)
                .foregroundColor(.white)
                .cornerRadius(10)
            }
            .padding()
            .background(.ultraThinMaterial)
        }
    }
}

/// Stats display item.
struct StatItem: View {
    let icon: String
    let value: String
    let label: String

    var body: some View {
        VStack(spacing: 4) {
            Image(systemName: icon)
                .foregroundColor(.accentColor)
            Text(value)
                .font(.headline)
            Text(label)
                .font(.caption)
                .foregroundColor(.secondary)
        }
    }
}

/// Single review display.
struct ReviewRow: View {
    let review: Review

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                AsyncImage(url: review.imageURL) { image in
                    image
                        .resizable()
                        .aspectRatio(contentMode: .fill)
                } placeholder: {
                    Circle()
                        .fill(Color.gray.opacity(0.2))
                }
                .frame(width: 32, height: 32)
                .clipShape(Circle())

                VStack(alignment: .leading) {
                    Text(review.name)
                        .font(.subheadline)
                        .fontWeight(.medium)
                    HStack(spacing: 2) {
                        ForEach(1...5, id: \.self) { star in
                            Image(systemName: star <= review.rating ? "star.fill" : "star")
                                .font(.caption)
                                .foregroundColor(.yellow)
                        }
                    }
                }
            }

            Text(review.description)
                .font(.body)
                .foregroundColor(.secondary)
        }
        .padding(.vertical, 8)
    }
}
