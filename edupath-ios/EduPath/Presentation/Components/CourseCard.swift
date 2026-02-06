import SwiftUI

/// Card displaying course thumbnail and basic info.
struct CourseCard: View {
    let course: Course

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            // Thumbnail
            AsyncImage(url: course.imageURL) { image in
                image
                    .resizable()
                    .aspectRatio(16/9, contentMode: .fill)
            } placeholder: {
                Rectangle()
                    .fill(Color.gray.opacity(0.2))
                    .aspectRatio(16/9, contentMode: .fill)
            }
            .frame(width: 260, height: 146)
            .clipShape(RoundedRectangle(cornerRadius: 12))

            // Title
            Text(course.title)
                .font(.headline)
                .lineLimit(2)

            // Instructor
            if let instructor = course.instructor {
                Text(instructor.name)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }

            // Price and stats
            HStack {
                Text(course.formattedPrice)
                    .font(.subheadline)
                    .fontWeight(.semibold)
                    .foregroundColor(course.isFree ? .green : .primary)

                Spacer()

                Label("\(course.students)", systemImage: "person.2")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
        .frame(width: 260)
    }
}

/// Card displaying category icon and name.
struct CategoryCard: View {
    let category: Category

    var body: some View {
        VStack(spacing: 12) {
            // Icon placeholder - in production would use actual icon fonts
            Image(systemName: "folder.fill")
                .font(.system(size: 32))
                .foregroundColor(.accentColor)

            Text(category.name)
                .font(.headline)
                .lineLimit(1)

            Text("\(category.courseCount) courses")
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color.gray.opacity(0.1))
        .cornerRadius(12)
    }
}
