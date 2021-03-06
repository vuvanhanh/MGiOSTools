import UIKit
import Reusable

final class {{ name }}ViewController: UITableViewController, BindableType {
    
    // MARK: - IBOutlets
    
{% for p in properties %}
    @IBOutlet weak var {{ p.name }}Label: UILabel!
{% endfor %}

    // MARK: - Properties
    
    var viewModel: {{ name }}ViewModel!

    // MARK: - Life Cycle
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    deinit {
        logDeinit()
    }
    
    // MARK: - Methods

    func bindViewModel() {
        let input = {{ name }}ViewModel.Input(
            loadTrigger: Driver.just(())
        )
        let output = viewModel.transform(input)
    {% for p in properties %}
        output.{{ p.name }}
            .drive()
            .disposed(by: rx.disposeBag)
    {% endfor %}
    }
}

// MARK: - StoryboardSceneBased
extension {{ name }}ViewController: StoryboardSceneBased {
    static var sceneStoryboard = UIStoryboard()
}
